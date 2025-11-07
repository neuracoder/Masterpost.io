"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import {
  Upload,
  User,
  CreditCard,
  Download,
  Play,
  Pause,
  X,
  Check,
  ImageIcon,
  Package,
  Instagram,
  ShoppingBag,
  FileArchive,
} from "lucide-react"
import Link from "next/link"
import { ImageProcessingApi, apiClient, type JobStatus } from "@/lib/api"
import { mockAuth } from "@/lib/auth"
import ImageEditor from "@/components/ImageEditor"
import ProcessingStatus from "@/components/ProcessingStatus"
import ImageGallery from "@/components/ImageGallery"

export default function AppPage() {
  // API URL from environment variable
  const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [selectedPipeline, setSelectedPipeline] = useState<"amazon" | "instagram" | "ebay" | "">("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentJobId, setCurrentJobId] = useState<string | null>(null)
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [processedImages, setProcessedImages] = useState<any[]>([])
  const [isDownloadReady, setIsDownloadReady] = useState(false)
  const [showEditor, setShowEditor] = useState(false)
  const [editingImageUrl, setEditingImageUrl] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Shadow settings
  const [shadowEnabled, setShadowEnabled] = useState(false)
  const [shadowType, setShadowType] = useState<"drop" | "reflection" | "natural" | "auto">("drop")
  const [shadowIntensity, setShadowIntensity] = useState(0.5)

  // Premium processing toggle
  const [usePremium, setUsePremium] = useState(false)

  // Real-time processing progress
  const [processingProgress, setProcessingProgress] = useState({
    current: 0,
    total: 0,
    percentage: 0,
    status: 'idle'
  })

  // Upload analysis (image count and estimated time)
  const [uploadAnalysis, setUploadAnalysis] = useState<{
    total_images: number;
    estimated_time_seconds: number;
    estimated_time_formatted: string;
    files: any[];
  } | null>(null)

  // Set demo token for testing
  useEffect(() => {
    apiClient.setAuthToken('demo_token')
  }, [])

  // Poll for progress updates every 2 seconds while processing
  useEffect(() => {
    if (!currentJobId || processingProgress.status === 'completed') return

    const pollProgress = async () => {
      try {
        const response = await fetch(`${API_URL}/api/v1/progress/${currentJobId}`)

        if (!response.ok) {
          console.error(`Progress poll failed: HTTP ${response.status}`)
          return
        }

        const data = await response.json()

        setProcessingProgress({
          current: data.current,
          total: data.total,
          percentage: data.percentage,
          status: data.status
        })

        // Update main progress bar
        setProgress(data.percentage)

        // Stop polling if completed
        if (data.status === 'completed') {
          clearInterval(intervalId)
          // Check final status
          const statusResponse = await fetch(`${API_URL}/api/v1/status/${currentJobId}`)
          const statusData = await statusResponse.json()
          
          // Map backend response to expected format 
          console.log('Raw Status Data:', statusData);
          
          const mappedStatusData = {
            ...statusData,
            successful_files: statusData.successful_files?.map((file: any) => {
              console.log('Processing file:', file);
              
              // Si el archivo ya tiene el formato correcto, devolverlo como está
              if (typeof file === 'object' && file.success !== undefined) {
                console.log('File already in correct format:', file);
                return file;
              }

              // Mapear la estructura de acuerdo al tipo de dato
              const fileObj = typeof file === 'string' ? { processed: file } : file;
              console.log('File object after initial mapping:', fileObj);

              const mappedFile = {
                success: true,
                original: fileObj.original || fileObj.processed || fileObj.filename || 'unknown.jpg',
                processed: fileObj.processed || fileObj.filename || 'unknown.jpg',
                path: fileObj.path || `${fileObj.processed || fileObj.filename || 'unknown.jpg'}`,
                shadow_applied: fileObj.shadow_applied || false,
                shadow_type: fileObj.shadow_type || null
              };

              console.log('Mapped file:', mappedFile);
              return mappedFile;
            }) || []
          };
          
          console.log('Final Mapped Status Data:', mappedStatusData);
          
          if (!Array.isArray(mappedStatusData.successful_files)) {
            console.error('successful_files is not an array:', mappedStatusData.successful_files);
            mappedStatusData.successful_files = [];
          }
          setJobStatus(mappedStatusData);
          setIsDownloadReady(true)
          setIsProcessing(false)
        }
      } catch (error) {
        console.error('Progress poll error:', error)
      }
    }

    // Poll immediately, then every 2 seconds
    pollProgress()
    const intervalId = setInterval(pollProgress, 2000)

    return () => clearInterval(intervalId)
  }, [currentJobId, processingProgress.status])

  // Helper function to check if file is ZIP
  const isZipFile = (file: File) => {
    return file.type === 'application/zip' || file.name.toLowerCase().endsWith('.zip')
  }

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])

    // Validate file types and sizes
    const validFiles = files.filter(file => {
      const isValidType = file.type.startsWith('image/') || file.type === 'application/zip' || file.name.toLowerCase().endsWith('.zip')
      const isZip = file.type === 'application/zip' || file.name.toLowerCase().endsWith('.zip')
      const maxSize = isZip ? 500 * 1024 * 1024 : 50 * 1024 * 1024 // 500MB for ZIP, 50MB for images
      const isValidSize = file.size <= maxSize
      return isValidType && isValidSize
    })

    if (validFiles.length !== files.length) {
      setError('Some files were skipped (invalid type or too large - max 50MB for images, 500MB for ZIP)')
    }

    setUploadedFiles((prev) => [...prev, ...validFiles])
    setError(null)

    // Analyze uploaded files to get image count
    if (validFiles.length > 0) {
      try {
        console.log('🔍 Analyzing uploaded files...')
        const formData = new FormData()
        validFiles.forEach(file => formData.append('files', file))

        const response = await fetch(`${API_URL}/analyze-upload`, {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          console.error('Analysis failed:', response.statusText)
          return
        }

        const analysis = await response.json()
        console.log('📊 Analysis result:', analysis)
        setUploadAnalysis(analysis)

        // Show success message with image count
        if (analysis.total_images > 0) {
          console.log(`✅ Found ${analysis.total_images} image${analysis.total_images !== 1 ? 's' : ''} to process (~${analysis.estimated_time_formatted})`)
        }
      } catch (error) {
        console.error('Error analyzing files:', error)
      }
    }
  }

  const handleChooseFilesClick = (event: React.MouseEvent) => {
    event.preventDefault()
    console.log('Choose Files clicked') // Debug log
    if (fileInputRef.current) {
      console.log('FileInputRef found, clicking...') // Debug log
      fileInputRef.current.click()
    } else {
      console.log('FileInputRef not found') // Debug log
    }
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
    event.stopPropagation()
    console.log('Drag over detected') // Debug log
  }

  const handleDragEnter = (event: React.DragEvent) => {
    event.preventDefault()
    event.stopPropagation()
    console.log('Drag enter detected') // Debug log
  }

  const handleDragLeave = (event: React.DragEvent) => {
    event.preventDefault()
    event.stopPropagation()
    console.log('Drag leave detected') // Debug log
  }

  const handleDrop = async (event: React.DragEvent) => {
    event.preventDefault()
    event.stopPropagation()
    console.log('Drop detected') // Debug log

    const files = Array.from(event.dataTransfer.files)
    console.log('Files dropped:', files.length) // Debug log

    // Validate file types and sizes
    const validFiles = files.filter(file => {
      const isValidType = file.type.startsWith('image/') || file.type === 'application/zip' || file.name.toLowerCase().endsWith('.zip')
      const isZip = file.type === 'application/zip' || file.name.toLowerCase().endsWith('.zip')
      const maxSize = isZip ? 500 * 1024 * 1024 : 50 * 1024 * 1024 // 500MB for ZIP, 50MB for images
      const isValidSize = file.size <= maxSize
      return isValidType && isValidSize
    })

    if (validFiles.length !== files.length) {
      setError('Some files were skipped (invalid type or too large - max 50MB for images, 500MB for ZIP)')
    }

    setUploadedFiles((prev) => [...prev, ...validFiles])
    setError(null)

    // Analyze uploaded files to get image count
    if (validFiles.length > 0) {
      try {
        console.log('🔍 Analyzing dropped files...')
        const formData = new FormData()
        validFiles.forEach(file => formData.append('files', file))

        const response = await fetch(`${API_URL}/analyze-upload`, {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          console.error('Analysis failed:', response.statusText)
          return
        }

        const analysis = await response.json()
        console.log('📊 Analysis result:', analysis)
        setUploadAnalysis(analysis)

        // Show success message with image count
        if (analysis.total_images > 0) {
          console.log(`✅ Found ${analysis.total_images} image${analysis.total_images !== 1 ? 's' : ''} to process (~${analysis.estimated_time_formatted})`)
        }
      } catch (error) {
        console.error('Error analyzing files:', error)
      }
    }
  }

  const removeFile = (index: number) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index))
    setError(null)
  }

  const handleDownload = async () => {
    if (!currentJobId) return

    try {
      await ImageProcessingApi.downloadProcessedImages(
        currentJobId,
        `masterpost_${selectedPipeline}_${new Date().toISOString().split('T')[0]}.zip`
      )
    } catch (error) {
      console.error('Download error:', error)
      setError('Download failed. Please try again.')
    }
  }

  const resetProcessing = () => {
    setIsProcessing(false)
    setProgress(0)
    setCurrentJobId(null)
    setJobStatus(null)
    setIsDownloadReady(false)
    setError(null)
    setProcessedImages([])
  }

  const handleEditImage = (imageUrl: string) => {
    setEditingImageUrl(imageUrl)
    setShowEditor(true)
  }

  const handleSaveEdit = (editedImageUrl: string) => {
    // Update the processed images list with the edited image
    setProcessedImages(prev =>
      prev.map(img =>
        img.url === editingImageUrl ? { ...img, url: editedImageUrl, edited: true } : img
      )
    )
    setShowEditor(false)
    setEditingImageUrl(null)
  }

  const handleCloseEditor = () => {
    setShowEditor(false)
    setEditingImageUrl(null)
  }

  // Cleanup object URLs when component unmounts or files change
  useEffect(() => {
    return () => {
      uploadedFiles.forEach(file => {
        URL.revokeObjectURL(URL.createObjectURL(file))
      })
    }
  }, [uploadedFiles])

  const startProcessing = async () => {
    if (!selectedPipeline || uploadedFiles.length === 0) return

    console.log('🚀 ====== STARTING PROCESSING ======')
    console.log('📁 Uploaded files:', uploadedFiles)
    console.log('📁 Number of files:', uploadedFiles.length)
    console.log('🎯 Selected pipeline:', selectedPipeline)
    console.log('✨ Premium processing:', usePremium ? 'YES (Qwen API)' : 'NO (local rembg)')
    console.log('⚙️ Shadow enabled:', shadowEnabled)
    console.log('⚙️ Shadow type:', shadowType)
    console.log('⚙️ Shadow intensity:', shadowIntensity)

    setIsProcessing(true)
    setIsUploading(true)
    setProgress(0)
    setError(null)

    try {
      // Log file details
      uploadedFiles.forEach((file, index) => {
        console.log(`📎 File ${index + 1}:`, {
          name: file.name,
          type: file.type,
          size: file.size,
          lastModified: new Date(file.lastModified).toISOString()
        })
      })

      console.log('🌐 API Base URL:', process.env.NEXT_PUBLIC_API_URL || '')
      console.log('📤 Calling ImageProcessingApi.uploadAndProcess...')

      // Step 1: Upload files and start processing with progress tracking
      const result = await ImageProcessingApi.uploadAndProcess(
        uploadedFiles,
        selectedPipeline as 'amazon' | 'instagram' | 'ebay',
        {
          quality: 95,
          // Premium processing toggle
          use_premium: usePremium,
          // Shadow settings
          shadow_enabled: shadowEnabled,
          shadow_type: shadowType,
          shadow_intensity: shadowIntensity,
          shadow_angle: 315,
          shadow_distance: 20,
          shadow_blur: 15,
          // Pipeline-specific settings
          ...(selectedPipeline === 'instagram' && { saturation: 1.3, apply_vignette: false }),
          ...(selectedPipeline === 'amazon' && { remove_background: true, optimize_coverage: true }),
          ...(selectedPipeline === 'ebay' && { clean_background: true, reduce_noise: true })
        },
        // Upload progress callback
        (progress) => {
          console.log(`📊 Upload progress: ${progress}%`)
          setUploadProgress(progress)
        }
      )

      console.log('✅ Upload result:', result)

      if (result.error || !result.jobId) {
        console.error('❌ Upload failed:', result.error)
        throw new Error(result.error || 'Failed to start processing')
      }

      console.log('✅ Job ID received:', result.jobId)
      setCurrentJobId(result.jobId)
      setIsUploading(false)
      setUploadProgress(0) // Reset upload progress

      console.log('🔄 Starting to poll job status...')

      // Step 2: Start polling for progress
      await ImageProcessingApi.pollJobStatus(
        result.jobId,
        (status: JobStatus) => {
          console.log('📊 Job status update:', status)
          setJobStatus(status)
          setProgress(status.progress_percentage)

          // Update UI based on status
          if (status.status === 'completed') {
            console.log('✅ Processing completed!')
            setIsProcessing(false)
            setIsDownloadReady(true)
          } else if (status.status === 'failed') {
            console.error('❌ Processing failed:', status.error_message)
            setIsProcessing(false)
            setError(status.error_message || 'Processing failed')
          }
        }
      )

    } catch (error) {
      console.error('💥 ====== PROCESSING ERROR ======')
      console.error('Error object:', error)
      console.error('Error message:', error instanceof Error ? error.message : 'Unknown error')
      console.error('Error stack:', error instanceof Error ? error.stack : 'No stack trace')
      setError(error instanceof Error ? error.message : 'Processing failed')
      setIsProcessing(false)
      setIsUploading(false)
      setUploadProgress(0) // Reset upload progress on error
    }
  }

  const pipelines: Array<{
    id: "amazon" | "instagram" | "ebay";
    name: string;
    description: string;
    features: string[];
    icon: any;
    color: string;
  }> = [
    {
      id: "amazon",
      name: "Amazon Compliant",
      description: "White background, 1000x1000px, 85% product coverage",
      features: ["Removes background", "Centers product", "Meets Amazon requirements"],
      icon: Package,
      color: "from-orange-500 to-orange-600",
    },
    {
      id: "instagram",
      name: "Instagram Ready",
      description: "1080x1080px, Perfect square, Enhanced colors",
      features: ["Square format", "Color boost", "Mobile optimized"],
      icon: Instagram,
      color: "from-pink-500 to-purple-600",
    },
    {
      id: "ebay",
      name: "eBay Optimized",
      description: "1600x1600px, Multiple angles, Zoom ready",
      features: ["High resolution", "Gallery ready", "Watermark friendly"],
      icon: ShoppingBag,
      color: "from-blue-500 to-blue-600",
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center">
              <Upload className="w-4 h-4 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">Masterpost.io</span>
          </Link>

          <div className="flex items-center space-x-4">
            <Badge className="bg-emerald-50 text-emerald-700 border-emerald-200">
              <CreditCard className="w-3 h-3 mr-1" />
              485 credits remaining
            </Badge>
            <Button variant="ghost" size="sm">
              <User className="w-4 h-4 mr-2" />
              Account
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Process Your Images</h1>
          <p className="text-gray-600">Upload your product photos and transform them with professional pipelines</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Upload Section */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Upload className="w-5 h-5 mr-2 text-emerald-600" />
                  Upload Images
                </CardTitle>
                <CardDescription>
                Drop up to 500 images (JPG, PNG, WebP) or ZIP files (max 500MB) or click to browse
                {isUploading && " • Uploading..."}
              </CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                    uploadedFiles.length > 0
                      ? "border-emerald-300 bg-emerald-50"
                      : "border-gray-300 hover:border-emerald-300 hover:bg-emerald-50"
                  }`}
                  onDragOver={handleDragOver}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <ImageIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-lg font-medium text-gray-900 mb-2">Drop your images or ZIP files here</p>
                  <p className="text-gray-500 mb-4">Support for individual images and ZIP archives</p>
                  <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept="image/*,.zip"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload">
                    <Button
                      type="button"
                      onClick={handleChooseFilesClick}
                      className="bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white cursor-pointer"
                    >
                      Choose Files
                    </Button>
                  </label>
                </div>

                {/* Upload Progress Bar */}
                {isUploading && uploadProgress > 0 && (
                  <div className="mt-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Uploading files...</span>
                      <span className="text-sm font-semibold text-emerald-600">{uploadProgress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-3 rounded-full transition-all duration-300 ease-out flex items-center justify-end"
                        style={{ width: `${uploadProgress}%` }}
                      >
                        {uploadProgress > 15 && (
                          <span className="text-white text-xs font-medium px-2">{uploadProgress}%</span>
                        )}
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {uploadProgress < 100 ? 'Please wait while your files are being uploaded...' : 'Upload complete! Starting processing...'}
                    </p>
                  </div>
                )}

                {/* Error Message */}
                {error && (
                  <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                )}

                {uploadedFiles.length > 0 && (
                  <div className="mt-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-medium text-gray-900">Uploaded Files ({uploadedFiles.length})</h3>
                      <div className="flex items-center gap-2">
                        {uploadAnalysis && uploadAnalysis.total_images > 0 && (
                          <Badge variant="outline" className="text-blue-700 border-blue-200 bg-blue-50">
                            {uploadAnalysis.total_images} image{uploadAnalysis.total_images !== 1 ? 's' : ''} • ~{uploadAnalysis.estimated_time_formatted}
                          </Badge>
                        )}
                        <Badge variant="outline" className="text-emerald-700 border-emerald-200">
                          {Math.round(uploadedFiles.reduce((acc, file) => acc + file.size, 0) / 1024 / 1024)} MB total
                        </Badge>
                        {uploadedFiles.reduce((acc, file) => acc + file.size, 0) > 200 * 1024 * 1024 && (
                          <Badge variant="outline" className="text-orange-600 border-orange-200 bg-orange-50">
                            Large upload - may take 1-2 min
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-h-64 overflow-y-auto">
                      {uploadedFiles.map((file, index) => (
                        <div key={index} className="relative group">
                          <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden flex items-center justify-center">
                            {isZipFile(file) ? (
                              <div className="flex flex-col items-center justify-center p-4">
                                <FileArchive className="w-8 h-8 text-blue-600 mb-2" />
                                <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">
                                  ZIP
                                </Badge>
                              </div>
                            ) : (
                              <img
                                src={URL.createObjectURL(file) || "/placeholder.svg"}
                                alt={file.name}
                                className="w-full h-full object-cover"
                              />
                            )}
                          </div>
                          <button
                            onClick={() => removeFile(index)}
                            className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                          >
                            <X className="w-3 h-3" />
                          </button>
                          <p className="text-xs text-gray-500 mt-1 truncate">{file.name}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Pipeline Selection */}
            <Card>
              <CardHeader>
                <CardTitle>Select Processing Pipeline</CardTitle>
                <CardDescription>Choose the optimization that best fits your marketplace</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-3 gap-4">
                  {pipelines.map((pipeline) => {
                    const Icon = pipeline.icon
                    return (
                      <div
                        key={pipeline.id}
                        className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                          selectedPipeline === pipeline.id
                            ? "border-emerald-300 bg-emerald-50 ring-2 ring-emerald-200"
                            : "border-gray-200 hover:border-emerald-200 hover:bg-emerald-50"
                        }`}
                        onClick={() => setSelectedPipeline(pipeline.id)}
                      >
                        <div
                          className={`w-10 h-10 bg-gradient-to-r ${pipeline.color} rounded-lg flex items-center justify-center mb-3`}
                        >
                          <Icon className="w-5 h-5 text-white" />
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">{pipeline.name}</h3>
                        <p className="text-sm text-gray-600 mb-3">{pipeline.description}</p>
                        <ul className="space-y-1">
                          {pipeline.features.map((feature, index) => (
                            <li key={index} className="flex items-center text-xs text-gray-500">
                              <Check className="w-3 h-3 text-emerald-500 mr-2" />
                              {feature}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>

            {/* Premium Processing Toggle */}
            <Card className="border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-blue-50">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <span className="mr-2">✨</span>
                  Premium AI Processing
                </CardTitle>
                <CardDescription>Advanced AI for complex backgrounds & fine details</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between p-4 bg-white rounded-lg border-2 border-purple-100">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                      <span className="text-2xl">🚀</span>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Use Premium Processing</h4>
                      <p className="text-sm text-gray-600">Qwen AI - Best for glass, jewelry, complex items</p>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={usePremium}
                      onChange={(e) => setUsePremium(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-14 h-7 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-purple-600 peer-checked:to-blue-600"></div>
                  </label>
                </div>

                {/* Pricing Info */}
                <div className="mt-4 p-4 bg-white rounded-lg border border-gray-200">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <p className="text-sm font-medium text-gray-700">Cost per image:</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {usePremium ? (
                          <>
                            <span className="font-semibold text-purple-600">3 credits</span> ($0.30/image)
                          </>
                        ) : (
                          <>
                            <span className="font-semibold text-green-600">1 credit</span> ($0.10/image)
                          </>
                        )}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-700">Processing method:</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {usePremium ? (
                          <span className="font-semibold text-purple-600">Qwen API</span>
                        ) : (
                          <span className="font-semibold text-green-600">Local rembg</span>
                        )}
                      </p>
                    </div>
                  </div>

                  {/* Features comparison */}
                  <div className="border-t pt-3">
                    {usePremium ? (
                      <div className="space-y-2">
                        <p className="text-sm font-medium text-purple-700">✨ Premium Features:</p>
                        <ul className="text-xs text-gray-600 space-y-1 ml-4">
                          <li>• Superior edge quality (hair, fur)</li>
                          <li>• Perfect for glass & transparent items</li>
                          <li>• Complex background handling</li>
                          <li>• AI-powered detail preservation</li>
                        </ul>
                      </div>
                    ) : (
                      <div className="space-y-2">
                        <p className="text-sm font-medium text-green-700">⚡ Basic Features:</p>
                        <ul className="text-xs text-gray-600 space-y-1 ml-4">
                          <li>• Fast local processing</li>
                          <li>• Good for simple backgrounds</li>
                          <li>• Solid colors & products</li>
                          <li>• Cost-effective bulk processing</li>
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Shadow Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <span className="mr-2">✨</span>
                  Shadow Effects (Optional)
                </CardTitle>
                <CardDescription>Add professional shadows to your product images</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Enable Shadow Toggle */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center">
                      <span className="text-xl">🌟</span>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">Enable Shadows</h4>
                      <p className="text-sm text-gray-500">Add depth to your images</p>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={shadowEnabled}
                      onChange={(e) => setShadowEnabled(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-emerald-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
                  </label>
                </div>

                {/* Shadow Type Selection */}
                {shadowEnabled && (
                  <div className="space-y-3 animate-in fade-in duration-300">
                    <label className="block text-sm font-medium text-gray-700">Shadow Type</label>
                    <div className="grid grid-cols-2 gap-3">
                      <div
                        className={`border-2 rounded-lg p-3 cursor-pointer transition-all ${
                          shadowType === 'drop'
                            ? 'border-purple-500 bg-purple-50'
                            : 'border-gray-200 hover:border-purple-300'
                        }`}
                        onClick={() => setShadowType('drop')}
                      >
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">📦</span>
                          <div>
                            <h5 className="font-medium text-sm">Drop Shadow</h5>
                            <p className="text-xs text-gray-500">Amazon style</p>
                          </div>
                        </div>
                      </div>

                      <div
                        className={`border-2 rounded-lg p-3 cursor-pointer transition-all ${
                          shadowType === 'reflection'
                            ? 'border-purple-500 bg-purple-50'
                            : 'border-gray-200 hover:border-purple-300'
                        }`}
                        onClick={() => setShadowType('reflection')}
                      >
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">🪞</span>
                          <div>
                            <h5 className="font-medium text-sm">Reflection</h5>
                            <p className="text-xs text-gray-500">Mirror effect</p>
                          </div>
                        </div>
                      </div>

                      <div
                        className={`border-2 rounded-lg p-3 cursor-pointer transition-all ${
                          shadowType === 'natural'
                            ? 'border-purple-500 bg-purple-50'
                            : 'border-gray-200 hover:border-purple-300'
                        }`}
                        onClick={() => setShadowType('natural')}
                      >
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">☀️</span>
                          <div>
                            <h5 className="font-medium text-sm">Natural</h5>
                            <p className="text-xs text-gray-500">Soft lighting</p>
                          </div>
                        </div>
                      </div>

                      <div
                        className={`border-2 rounded-lg p-3 cursor-pointer transition-all ${
                          shadowType === 'auto'
                            ? 'border-purple-500 bg-purple-50'
                            : 'border-gray-200 hover:border-purple-300'
                        }`}
                        onClick={() => setShadowType('auto')}
                      >
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">🤖</span>
                          <div>
                            <h5 className="font-medium text-sm">Auto</h5>
                            <p className="text-xs text-gray-500">AI selects</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Shadow Intensity */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-700">Shadow Intensity</label>
                        <span className="text-sm text-gray-500">{Math.round(shadowIntensity * 100)}%</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.1"
                        value={shadowIntensity}
                        onChange={(e) => setShadowIntensity(parseFloat(e.target.value))}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
                      />
                      <div className="flex justify-between text-xs text-gray-500">
                        <span>Light</span>
                        <span>Medium</span>
                        <span>Strong</span>
                      </div>
                    </div>

                    {/* Preview Info */}
                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-3">
                      <div className="flex items-start space-x-2">
                        <span className="text-purple-600 mt-0.5">ℹ️</span>
                        <div className="text-xs text-purple-800">
                          <p className="font-medium mb-1">Shadow Preview:</p>
                          <p>
                            <strong>{shadowType === 'drop' ? 'Drop Shadow' : shadowType === 'reflection' ? 'Reflection' : shadowType === 'natural' ? 'Natural' : 'Auto-detect'}</strong> at {Math.round(shadowIntensity * 100)}% intensity
                          </p>
                          {shadowType === 'auto' && (
                            <p className="mt-1 text-purple-600">AI will analyze each image and apply the best shadow type</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Processing Controls */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-gray-900">Ready to Process</h3>
                    <p className="text-sm text-gray-500">
                      {uploadedFiles.length} images •{" "}
                      {selectedPipeline
                        ? pipelines.find((p) => p.id === selectedPipeline)?.name
                        : "No pipeline selected"}
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    {isDownloadReady && (
                      <Button
                        onClick={resetProcessing}
                        variant="outline"
                        className="bg-transparent"
                      >
                        Process New Batch
                      </Button>
                    )}
                    <Button
                      onClick={startProcessing}
                      disabled={!selectedPipeline || uploadedFiles.length === 0 || isProcessing}
                      className="bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white"
                    >
                      {isUploading ? (
                        <>
                          <Upload className="w-4 h-4 mr-2 animate-pulse" />
                          Uploading...
                        </>
                      ) : isProcessing ? (
                        <>
                          <Pause className="w-4 h-4 mr-2" />
                          Processing...
                        </>
                      ) : (
                        <>
                          <Play className="w-4 h-4 mr-2" />
                          Start Processing
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Progress & Results Sidebar */}
          <div className="space-y-6">
            {/* Processing Status - Always Visible */}
            <ProcessingStatus
              isProcessing={isProcessing || processingProgress.status === 'processing'}
              progress={processingProgress.percentage || progress}
              currentImage={processingProgress.current}
              totalImages={uploadAnalysis?.total_images || processingProgress.total || uploadedFiles.length}
              estimatedTotalTime={uploadAnalysis?.estimated_time_seconds}
              pipeline={selectedPipeline ? pipelines.find((p) => p.id === selectedPipeline)?.name || 'Amazon Compliant' : 'Amazon Compliant'}
            />

            {/* Download Section */}
            {isDownloadReady && currentJobId && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-emerald-900">Download Ready</CardTitle>
                  <CardDescription>
                    {jobStatus?.processed_files || uploadedFiles.length} images processed successfully
                    {jobStatus?.pipeline && ` • ${jobStatus.pipeline.charAt(0).toUpperCase() + jobStatus.pipeline.slice(1)} pipeline`}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-center p-8 bg-emerald-50 rounded-lg">
                    <div className="text-center">
                      <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <Check className="w-8 h-8 text-emerald-600" />
                      </div>
                      <h3 className="font-semibold text-emerald-900 mb-2">Processing Complete!</h3>
                      <p className="text-sm text-emerald-700">
                        {uploadedFiles.length === 1
                          ? 'Your processed image is ready'
                          : `Your ${uploadedFiles.length} processed images are ready`
                        }
                      </p>
                    </div>
                  </div>

                  {/* Processed Images Gallery - New Enhanced Preview */}
                  {jobStatus?.successful_files && jobStatus.successful_files.length > 0 && currentJobId && (
                    <div className="space-y-4">
                      <h4 className="font-medium text-gray-900 text-lg">
                        Processed Images ({jobStatus.successful_files.length})
                      </h4>
                      <ImageGallery
                        images={jobStatus.successful_files}
                        jobId={currentJobId}
                        isLoading={false}
                        maxVisibleImages={50}
                        columns={3}
                      />
                    </div>
                  )}

                  <Button
                    onClick={handleDownload}
                    className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    {uploadedFiles.length === 1 ? 'Download Image' : 'Download All as ZIP'}
                  </Button>

                  <div className="text-xs text-gray-500 text-center">
                    {uploadedFiles.length === 1
                      ? `File: masterpost_processed.${uploadedFiles[0]?.name.split('.').pop() || 'jpg'}`
                      : `ZIP: masterpost_batch_${uploadedFiles.length}_images.zip`
                    }
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Quick Stats */}
            <Card>
              <CardHeader>
                <CardTitle className="text-emerald-900">Quick Stats</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Images processed today</span>
                  <span className="font-semibold text-emerald-600">127</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Credits remaining</span>
                  <span className="font-semibold text-emerald-600">485</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Success rate</span>
                  <span className="font-semibold text-emerald-600">99.2%</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Image Editor Modal */}
      {showEditor && editingImageUrl && (
        <ImageEditor
          imageUrl={editingImageUrl}
          onSave={handleSaveEdit}
          onClose={handleCloseEditor}
        />
      )}
    </div>
  )
}

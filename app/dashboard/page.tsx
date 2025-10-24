"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Upload,
  User,
  CreditCard,
  Settings,
  History,
  BarChart3,
  TrendingUp,
  Download,
  Clock,
  CheckCircle,
  Package,
  Instagram,
  ShoppingBag,
  Menu,
  X,
} from "lucide-react"
import Link from "next/link"

export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const recentJobs = [
    {
      id: 1,
      name: "Product Photos Batch 1",
      pipeline: "Amazon Compliant",
      images: 45,
      status: "completed",
      date: "2 hours ago",
      downloadUrl: "#",
    },
    {
      id: 2,
      name: "Instagram Collection",
      pipeline: "Instagram Ready",
      images: 23,
      status: "processing",
      progress: 67,
      date: "5 minutes ago",
    },
    {
      id: 3,
      name: "eBay Listings Update",
      pipeline: "eBay Optimized",
      images: 78,
      status: "completed",
      date: "1 day ago",
      downloadUrl: "#",
    },
    {
      id: 4,
      name: "Summer Collection",
      pipeline: "Amazon Compliant",
      images: 12,
      status: "failed",
      date: "2 days ago",
      error: "Invalid file format",
    },
  ]

  const sidebarItems = [
    { name: "Dashboard", href: "/dashboard", icon: BarChart3, active: true },
    { name: "Process Images", href: "/app", icon: Upload, active: false },
    { name: "History", href: "/dashboard/history", icon: History, active: false },
    { name: "Settings", href: "/dashboard/settings", icon: Settings, active: false },
    { name: "Billing", href: "/dashboard/billing", icon: CreditCard, active: false },
  ]

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-800">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center">
              <Upload className="w-4 h-4 text-white" />
            </div>
            <span className="text-xl font-bold text-white">Masterpost.io</span>
          </Link>
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden text-gray-400 hover:text-white"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="w-5 h-5" />
          </Button>
        </div>

        <nav className="mt-8 px-4">
          <ul className="space-y-2">
            {sidebarItems.map((item) => {
              const Icon = item.icon
              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                      item.active ? "bg-emerald-600 text-white" : "text-gray-300 hover:bg-gray-800 hover:text-white"
                    }`}
                  >
                    <Icon className="w-5 h-5 mr-3" />
                    {item.name}
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-300">Credits</span>
                <span className="text-sm font-semibold text-emerald-400">485 / 500</span>
              </div>
              <Progress value={97} className="h-2 mb-2" />
              <Button size="sm" className="w-full bg-emerald-600 hover:bg-emerald-700 text-white">
                Upgrade Plan
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 lg:ml-0">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Button variant="ghost" size="sm" className="lg:hidden mr-4" onClick={() => setSidebarOpen(true)}>
                <Menu className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-gray-600">Welcome back! Here's your processing overview.</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge className="bg-emerald-50 text-emerald-700 border-emerald-200">
                <CreditCard className="w-3 h-3 mr-1" />
                Pro Plan
              </Badge>
              <Button variant="ghost" size="sm">
                <User className="w-4 h-4 mr-2" />
                Profile
              </Button>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Images This Month</p>
                    <p className="text-3xl font-bold text-emerald-600">1,247</p>
                  </div>
                  <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center">
                    <Upload className="w-6 h-6 text-emerald-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <TrendingUp className="w-4 h-4 text-emerald-500 mr-1" />
                  <span className="text-emerald-600 font-medium">+12%</span>
                  <span className="text-gray-500 ml-1">from last month</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Credits Remaining</p>
                    <p className="text-3xl font-bold text-emerald-600">485</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <CreditCard className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <span className="text-gray-500">of 500 total credits</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Success Rate</p>
                    <p className="text-3xl font-bold text-emerald-600">99.2%</p>
                  </div>
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <CheckCircle className="w-6 h-6 text-green-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <span className="text-gray-500">1,235 successful / 1,245 total</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Processing Time</p>
                    <p className="text-3xl font-bold text-emerald-600">2.3m</p>
                  </div>
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Clock className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4 text-sm">
                  <span className="text-gray-500">avg per batch</span>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Recent Jobs */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Processing Jobs</CardTitle>
                  <CardDescription>Your latest image processing activities</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentJobs.map((job) => (
                      <div key={job.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="flex items-center space-x-4">
                          <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                            {job.pipeline === "Amazon Compliant" && <Package className="w-5 h-5 text-orange-600" />}
                            {job.pipeline === "Instagram Ready" && <Instagram className="w-5 h-5 text-pink-600" />}
                            {job.pipeline === "eBay Optimized" && <ShoppingBag className="w-5 h-5 text-blue-600" />}
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-900">{job.name}</h4>
                            <div className="flex items-center space-x-2 text-sm text-gray-500">
                              <span>{job.pipeline}</span>
                              <span>•</span>
                              <span>{job.images} images</span>
                              <span>•</span>
                              <span>{job.date}</span>
                            </div>
                            {job.status === "processing" && (
                              <div className="mt-2">
                                <Progress value={job.progress} className="h-1 w-32" />
                                <span className="text-xs text-gray-500">{job.progress}% complete</span>
                              </div>
                            )}
                            {job.status === "failed" && <p className="text-xs text-red-600 mt-1">{job.error}</p>}
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          {job.status === "completed" && (
                            <>
                              <Badge className="bg-green-100 text-green-800">Completed</Badge>
                              <Button size="sm" variant="outline">
                                <Download className="w-3 h-3 mr-1" />
                                Download
                              </Button>
                            </>
                          )}
                          {job.status === "processing" && (
                            <Badge className="bg-blue-100 text-blue-800">Processing</Badge>
                          )}
                          {job.status === "failed" && <Badge className="bg-red-100 text-red-800">Failed</Badge>}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-6">
                    <Button variant="outline" className="w-full bg-transparent">
                      View All Jobs
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Usage Chart & Quick Actions */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Credit Usage</CardTitle>
                  <CardDescription>Last 30 days</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Amazon Pipeline</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div className="bg-orange-500 h-2 rounded-full" style={{ width: "65%" }}></div>
                        </div>
                        <span className="text-sm font-medium text-gray-900">325</span>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Instagram Pipeline</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div className="bg-pink-500 h-2 rounded-full" style={{ width: "45%" }}></div>
                        </div>
                        <span className="text-sm font-medium text-gray-900">225</span>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">eBay Pipeline</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div className="bg-blue-500 h-2 rounded-full" style={{ width: "30%" }}></div>
                        </div>
                        <span className="text-sm font-medium text-gray-900">150</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white">
                    <Upload className="w-4 h-4 mr-2" />
                    Process New Images
                  </Button>
                  <Button variant="outline" className="w-full bg-transparent">
                    <History className="w-4 h-4 mr-2" />
                    View Processing History
                  </Button>
                  <Button variant="outline" className="w-full bg-transparent">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Upgrade Plan
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}
    </div>
  )
}

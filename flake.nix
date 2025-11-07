{
  description = "Python environment for Masterpost-SaaS";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
      };
      pythonPackages = ps: with ps; [
        fastapi
        uvicorn
        python-multipart
        aiofiles
        python-jose
        passlib
        pyjwt
        bcrypt
        sqlalchemy
        psycopg2
        supabase
        stripe
        rembg
        pillow
        numpy
        opencv-python-headless
        dashscope
        requests
        python-dotenv
        pydantic
        pydantic-settings
        httpx
        celery
        redis
        pytest
        pytest-asyncio
        typing-extensions
        email-validator
        onnxruntime
        filetype
      ];
      python-with-packages = pkgs.python3.withPackages pythonPackages;
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          python-with-packages
        ];
      };
    };
}

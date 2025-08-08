# 🐳 Docker Setup for AI Image Generator Backend

This guide helps you set up the MinIO object storage infrastructure for your AI Image Generator backend.

## 🚀 Quick Start

### 1. Copy Environment Variables
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your real Gemini API key
# The MinIO settings are already configured for local development
```

### 2. Start MinIO
```bash
# Start MinIO container
docker-compose up -d

# Check if containers are running
docker-compose ps
```

### 3. Access MinIO Console
- **MinIO Console (Web UI)**: http://localhost:9001
- **MinIO API**: http://localhost:9000
- **Username**: `minioadmin`
- **Password**: `minioadmin123`

## 📁 What Gets Created

The docker-compose setup creates:
- **MinIO Server**: Object storage API on port 9000
- **MinIO Console**: Web UI on port 9001  
- **Bucket**: `ai-images` (automatically created)
- **Public Policy**: Set on the bucket for easy access
- **Persistent Storage**: Data persists between container restarts

## 🔧 Configuration Alignment

The docker-compose configuration aligns perfectly with your codebase:

| Backend Code | Docker Config | Description |
|-------------|---------------|-------------|
| `OBJECT_STORAGE_ENDPOINT` | `localhost:9000` | MinIO API endpoint |
| `OBJECT_STORAGE_BUCKET` | `ai-images` | Bucket for storing generated images |
| `OBJECT_STORAGE_ACCESS_KEY` | `minioadmin` | Access credentials |
| `OBJECT_STORAGE_SECRET_KEY` | `minioadmin123` | Secret credentials |
| `USE_HTTPS` | `false` | Local development uses HTTP |

## 🛠️ Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs minio

# Reset everything (CAUTION: deletes data)
docker-compose down -v

# Check MinIO health
curl http://localhost:9000/minio/health/live
```

## 🔍 Troubleshooting

### MinIO won't start
- Check if ports 9000/9001 are already in use
- Verify Docker is running

### Cannot connect from backend
- Ensure both containers are on the same network
- Check the endpoint configuration matches `.env`

### Bucket not found
- The setup container should create the bucket automatically
- If not, create it manually via the web console

## 🎯 Next Steps

With MinIO running, you can:
1. Test the storage provider connection
2. Upload test images via the console
3. Move to implementing the services layer
4. Build the FastAPI endpoints

Your `MinioStorageProvider` class is ready to connect to this infrastructure!

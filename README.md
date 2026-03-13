# 🎭 VTuber Wiki API

> **📚 ACADEMIC PROJECT — For Educational Use Only**

<div align="center">
  
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
  [![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
  
  <p><i>A comprehensive RESTful API serving as a public database for Virtual YouTuber (VTuber) profiles and agencies</i></p>
  
  **[Explore the Docs](#api-endpoints) • [Report Bug](https://github.com/stingy-namake/vtuber-api/issues) • [Request Feature](https://github.com/stingy-namake/vtuber-api/issues)**

</div>

---

## ⚠️ Important Disclaimer

This project was developed **exclusively for academic purposes** as a college assignment to demonstrate API development skills. It is **not production-ready** and should not be deployed in real-world scenarios. The author acknowledges potential security vulnerabilities, reliability issues, and performance limitations.

---

## 🎯 Overview

The VTuber Wiki API provides structured access to information about Virtual YouTubers, their affiliated agencies, social media presence, and more. Built with modern technologies and best practices, this project showcases:

- ✅ **RESTful architecture** with proper HTTP semantics
- ✅ **Role-based access control** (public read vs. protected write)
- ✅ **Comprehensive CRUD operations** with bulk endpoints
- ✅ **Advanced search and filtering** capabilities
- ✅ **JWT authentication** for secure write operations

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔓 **Public Read Access** | All GET endpoints freely accessible without authentication |
| 🔒 **Protected Write Operations** | POST, PUT, DELETE require valid Supabase JWT authentication |
| 📊 **Comprehensive VTuber Data** | Store agency info, debut dates, social links, tags, and more |
| 🔍 **Advanced Search** | Full-text search across names and descriptions with agency filtering |
| 📦 **Bulk Operations** | Create multiple VTuber entries in a single request |
| 🔄 **Pagination Support** | Efficiently browse through large datasets |

---

## 🛠️ Technology Stack

<div align="center">
  
| | | |
|---|---|---|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com) | High-performance Python async framework |
| **Database** | [Supabase](https://supabase.com) | PostgreSQL with real-time capabilities |
| **Authentication** | [Supabase Auth](https://supabase.com/auth) | JWT-based authentication system |
| **API Testing** | [Postman](https://postman.com) | Comprehensive API testing suite |
| **Deployment** | [Vercel](https://vercel.com) / [Render](https://render.com) | Serverless-ready deployment |

</div>

---

## 📋 API Endpoints

### Public Routes (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Interactive API documentation |
| `GET` | `/health` | Service health check |
| `GET` | `/vtubers` | List all VTubers (paginated) |
| `GET` | `/vtubers/{id}` | Retrieve specific VTuber |
| `GET` | `/search` | Full-text search across VTubers |
| `GET` | `/agencies` | List all unique agencies |

### Protected Routes (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/vtubers` | Create a single VTuber |
| `POST` | `/vtubers/bulk` | Create multiple VTubers (wrapped array) |
| `POST` | `/vtubers/batch` | ⚠️ WIP — Batch creation (direct array) |
| `PUT` | `/vtubers/{id}` | Update VTuber information |
| `DELETE` | `/vtubers/{id}` | Remove VTuber from database |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Supabase account with a `vtubers` table
- Postman (for testing)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/stingy-namake/vtuber-api.git
   cd vtuber-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

4. **Run the development server**
   ```bash
   uvicorn main:app --reload
   ```

---

## 🧪 Testing Guide

### Postman Environment Setup

Create a Postman environment with these variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `api_url` | API base URL | `http://localhost:8000` |
| `supabase_url` | Your Supabase URL | `https://xyz.supabase.co` |
| `api_key` | Supabase anon key | `eyJhbGciOiJIUzI1NiIs...` |
| `access_token` | JWT token (auto-filled) | — |
| `user_id` | Authenticated user ID | — |
| `vtuber_id` | Created VTuber ID | — |

### Testing Workflow

<details>
<summary><b>📌 Step 1: Verify Public Endpoints</b></summary>

- `GET /` — Confirm API is running
- `GET /health` — Check service status
- `GET /vtubers` — Verify database connection
</details>

<details>
<summary><b>🔐 Step 2: Authentication Setup</b></summary>

- Create user account via Supabase Auth
- Login to obtain access token
- Token auto-populates in environment
</details>

<details>
<summary><b>✍️ Step 3: Test Protected Operations</b></summary>

- Create single VTuber with `POST /vtubers`
- Verify creation with `GET /vtubers`
- Update data with `PUT /vtubers/{id}`
- Test search functionality
</details>

<details>
<summary><b>📦 Step 4: Bulk Operations</b></summary>

- Use `POST /vtubers/bulk` for wrapped array format
- ⚠️ Test `POST /vtubers/batch` (WIP)
- Verify all entries were created
</details>

<details>
<summary><b>🧹 Step 5: Cleanup</b></summary>

- Delete test data with `DELETE /vtubers/{id}`
- Logout to invalidate token
</details>

---

## 📊 Data Model

### VTuber Object Schema

```json
{
  "name": "Gawr Gura",
  "agency": "hololive English",
  "debut_date": "2020-09-13",
  "description": "A descendant of the Lost City of Atlantis",
  "image_url": "https://example.com/gura.jpg",
  "youtube_channel": "UCQ0UDLQCjY0rmuxCDE38FGg",
  "twitter_handle": "gawrgura",
  "tags": ["hololive", "english", "shark", "gaming"]
}
```

### Database Schema

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `id` | UUID | ✅ | Primary key |
| `name` | VARCHAR | ✅ | VTuber name |
| `agency` | VARCHAR | ❌ | Agency affiliation |
| `debut_date` | DATE | ❌ | Debut date |
| `description` | TEXT | ❌ | VTuber biography |
| `image_url` | TEXT | ❌ | Profile image |
| `youtube_channel` | TEXT | ❌ | YouTube channel ID |
| `twitter_handle` | VARCHAR | ❌ | Twitter/X handle |
| `tags` | TEXT[] | ❌ | Categorization tags |
| `created_at` | TIMESTAMP | ✅ | Auto-generated |
| `updated_at` | TIMESTAMP | ✅ | Auto-updated |

---

## 🔄 Error Handling

The API follows standard HTTP status code conventions:

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | Success | Request processed successfully |
| `201` | Created | Resource successfully created |
| `400` | Bad Request | Malformed request syntax |
| `401` | Unauthorized | Missing or invalid authentication |
| `404` | Not Found | Resource doesn't exist |
| `500` | Internal Error | Server-side failure |

---

## 🤝 Contributing

While this is an academic project, contributions for educational purposes are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📬 Contact

Project Link: [https://github.com/stingy-namake/vtuber-api](https://github.com/stingy-namake/vtuber-api)

---

<div align="center">
  
  **⭐ Star this repository if you find it useful for learning! ⭐**
  
  <sub>Built with ❤️ for educational purposes | College Assignment Project</sub>
  
</div>

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Test server is running"}

@app.get("/api/youtube/trending")
def get_trending():
    return {
        "trending_videos": [
            {
                "title": "테스트 동영상 1",
                "category": "게임",
                "trend_score": 95,
                "views": 1000000,
                "thumbnail": "🎮"
            }
        ],
        "count": 1,
        "source": "test_data"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

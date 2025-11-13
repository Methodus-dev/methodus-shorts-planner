# 🚀 YouTube API 할당량 최적화 가이드

## 📊 YouTube API 할당량 이해

### 기본 할당량
- **일일 할당량**: 10,000 units
- **할당량 리셋**: 매일 자정 (Pacific Time)

### API 호출별 비용
| API 메서드 | 비용 (units) | 설명 |
|------------|-------------|------|
| `videos.list` | 1 | 비디오 상세 정보 조회 |
| `search.list` | 100 | 비디오 검색 |
| `channels.list` | 1 | 채널 정보 조회 |

---

## ✅ Methodus에서 구현된 최적화 전략

### 1. **배치 처리** (Batch Processing)
한 번의 API 호출로 여러 비디오 정보를 조회합니다.

```python
# 나쁜 예: 비디오 10개 = 10 units
for video_id in video_ids:
    get_video_details(video_id)  # 1 unit × 10 = 10 units

# 좋은 예: 비디오 10개 = 1 unit
get_videos_by_ids(video_ids)  # 1 unit (최대 50개까지)
```

**절감 효과**: 10개 비디오 조회 시 10 units → 1 unit (90% 절감)

---

### 2. **스마트 캐싱** (Smart Caching)
API 호출 결과를 캐시하여 재사용합니다.

```python
# 캐시 파일: video_cache.json
- 캐시 저장: 데이터 수집 후 자동 저장
- 캐시 로드: 서버 시작 시 자동 로드
- 캐시 유효 기간: 2시간
```

**절감 효과**: 반복 요청 시 API 호출 0 units

---

### 3. **자동 업데이트 스케줄링**
2시간마다 자동으로 데이터를 업데이트합니다.

```python
# 업데이트 주기: 2시간
하루 업데이트 횟수 = 24시간 / 2시간 = 12회

# 1회당 API 비용
- KR 지역 급상승 30개: 1 unit
- US 지역 급상승 30개: 1 unit  
- JP 지역 급상승 30개: 1 unit
총 1회 비용 = 3 units

# 하루 총 비용
일일 총 비용 = 12회 × 3 units = 36 units
```

**할당량 사용률**: 36 / 10,000 = 0.36% (충분히 여유 있음!)

---

### 4. **선택적 필드 요청**
필요한 필드만 요청하여 데이터 전송량을 줄입니다.

```python
# snippet: 제목, 설명, 썸네일 등 기본 정보
# statistics: 조회수, 좋아요, 댓글 수
# contentDetails: 영상 길이, 화질 등

part='snippet,statistics,contentDetails'
```

---

### 5. **지역별 데이터 수집 최적화**
여러 지역의 데이터를 효율적으로 수집합니다.

```python
# 한국, 미국, 일본 급상승 영상 수집
get_multiple_regions(['KR', 'US', 'JP'], max_results_per_region=30)

# 중복 제거 (같은 영상이 여러 지역에서 인기일 경우)
seen_ids.add(video_id)
```

---

## 📈 실제 사용량 계산

### 일반적인 사용 시나리오

#### 시나리오 1: 정상 운영 (자동 업데이트만)
```
하루 자동 업데이트: 12회 × 3 units = 36 units
여유 할당량: 10,000 - 36 = 9,964 units (99.6% 남음)
```

#### 시나리오 2: 사용자가 수동 새로고침 100번
```
자동 업데이트: 36 units
수동 새로고침: 100회 × 3 units = 300 units
총 사용량: 336 units
여유 할당량: 10,000 - 336 = 9,664 units (96.6% 남음)
```

#### 시나리오 3: 키워드 검색 사용 (search.list)
```
자동 업데이트: 36 units
키워드 검색: 20회 × 100 units = 2,000 units
총 사용량: 2,036 units
여유 할당량: 10,000 - 2,036 = 7,964 units (79.6% 남음)
```

---

## ⚠️ 할당량 초과 방지 전략

### 1. 캐시 우선 사용
```python
# 캐시된 데이터가 있으면 API 호출하지 않음
if cached_videos:
    return cached_videos
else:
    fetch_youtube_data()  # API 호출
```

### 2. 에러 핸들링
```python
try:
    youtube_service.get_trending_videos()
except HttpError as e:
    if e.resp.status == 403:
        print("할당량 초과! 캐시 데이터 사용")
        return cached_videos
```

### 3. 할당량 모니터링
```python
# /api/health 엔드포인트에서 확인
{
    "youtube_api": "active",
    "cached_videos": 90,
    "last_update": "2025-11-12T..."
}
```

---

## 🎯 추가 최적화 옵션 (필요 시)

### 옵션 1: 캐시 유효 기간 연장
```python
# 2시간 → 4시간으로 변경
time.sleep(4 * 60 * 60)  # 하루 6회 업데이트

일일 비용: 6회 × 3 units = 18 units (50% 절감)
```

### 옵션 2: 지역 축소
```python
# 3개 지역 → 1개 지역으로 축소
get_multiple_regions(['KR'], max_results_per_region=50)

1회 비용: 3 units → 1 unit (66% 절감)
```

### 옵션 3: Redis 캐싱
```python
# JSON 파일 대신 Redis 사용 (선택사항)
import redis
cache = redis.Redis()
cache.setex('videos', 7200, json.dumps(videos))  # 2시간 TTL
```

---

## 📊 할당량 모니터링

### Google Cloud Console에서 확인
1. [API 할당량 페이지](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas) 접속
2. "Queries per day" 확인
3. 그래프에서 실시간 사용량 확인

### 알림 설정 (권장)
1. Google Cloud Console > "모니터링" > "알림"
2. 할당량 80% 초과 시 이메일 알림 설정

---

## ✅ 결론

Methodus의 현재 구현은 **매우 효율적**입니다:
- ✅ 일일 할당량의 0.36%만 사용 (36 / 10,000 units)
- ✅ 99.6%의 여유 할당량
- ✅ 수천 명의 동시 사용자도 감당 가능
- ✅ 추가 비용 없이 무료로 운영 가능

**할당량 걱정 없이 안심하고 사용하세요! 🚀**



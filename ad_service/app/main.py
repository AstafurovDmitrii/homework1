from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from typing import Dict, Optional, List
from app.models import Advertisement, AdvertisementUpdate

app = FastAPI()

# "База данных" в памяти
ads_db: Dict[int, Advertisement] = {}
current_id = 1

# POST /advertisement — создание объявления
@app.post("/advertisement")
async def create_ad(ad: Advertisement):
    global current_id
    ad.id = current_id
    ads_db[current_id] = ad
    current_id += 1
    return ad

# GET /advertisement/{ad_id} — получение по ID
@app.get("/advertisement/{ad_id}")
async def get_ad(ad_id: int):
    if ad_id not in ads_db:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ads_db[ad_id]

# PATCH /advertisement/{ad_id} — обновление
@app.patch("/advertisement/{ad_id}")
async def update_ad(ad_id: int, update_data: AdvertisementUpdate):
    if ad_id not in ads_db:
        raise HTTPException(status_code=404, detail="Ad not found")
    
    ad = ads_db[ad_id]
    update_dict = update_data.dict(exclude_unset=True)
    updated_ad = ad.copy(update=update_dict)
    ads_db[ad_id] = updated_ad
    return updated_ad

# DELETE /advertisement/{ad_id} — удаление
@app.delete("/advertisement/{ad_id}")
async def delete_ad(ad_id: int):
    if ad_id not in ads_db:
        raise HTTPException(status_code=404, detail="Ad not found")
    del ads_db[ad_id]
    return {"message": "Ad deleted"}

# GET /advertisement — поиск по полям
@app.get("/advertisement")
async def search_ads(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
):
    result = list(ads_db.values())
    
    if title:
        result = [ad for ad in result if title.lower() in ad.title.lower()]
    if author:
        result = [ad for ad in result if author.lower() in ad.author.lower()]
    if min_price is not None:
        result = [ad for ad in result if ad.price >= min_price]
    if max_price is not None:
        result = [ad for ad in result if ad.price <= max_price]
    
    return result
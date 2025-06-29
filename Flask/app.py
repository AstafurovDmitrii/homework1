from aiohttp import web
from datetime import datetime

app = web.Application()
ads_db = {}
current_id = 1

# POST /ads — создание объявления
async def create_ad(request):
    global current_id
    
    try:
        data = await request.json()
    except:
        return web.json_response(
            {"error": "Invalid JSON"}, 
            status=400
        )
    
    if not data or 'title' not in data or 'owner' not in data:
        return web.json_response(
            {"error": "Title and owner are required"}, 
            status=400
        )
    
    ad = {
        "id": current_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "owner": data["owner"]
    }
    
    ads_db[current_id] = ad
    current_id += 1
    
    return web.json_response(ad, status=201)

# GET /ads/{id} — получение объявления
async def get_ad(request):
    ad_id = int(request.match_info['ad_id'])
    ad = ads_db.get(ad_id)
    
    if not ad:
        return web.json_response(
            {"error": "Ad not found"}, 
            status=404
        )
    
    return web.json_response(ad)

# DELETE /ads/{id} — удаление объявления
async def delete_ad(request):
    ad_id = int(request.match_info['ad_id'])
    
    if ad_id not in ads_db:
        return web.json_response(
            {"error": "Ad not found"}, 
            status=404
        )
    
    del ads_db[ad_id]
    return web.json_response(
        {"message": "Ad deleted"}, 
        status=200
    )

# Регистрация роутов
app.router.add_post('/ads', create_ad)
app.router.add_get('/ads/{ad_id}', get_ad)
app.router.add_delete('/ads/{ad_id}', delete_ad)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
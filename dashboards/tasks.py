import aiohttp
from celery import shared_task

@shared_task
async def get_Vulnerabilities(host_id):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2000)) as session:
        async with session.post(f"http://127.0.0.1:8080/api/cves/{host_id}") as resp:
            data = await resp.json()
    
    return data

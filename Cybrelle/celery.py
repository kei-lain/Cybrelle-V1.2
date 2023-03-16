
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cybrelle.settings')

app = Celery('Cybrelle', broker='rediss://default:AVNS_iVcSzA7isfKzUUSOrrp@cybrelle-celery-redis-do-user-13199386-0.b.db.ondigitalocean.com:25061')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def getVulnerabilities(self, request, host_id):
    """
    Celery task to retrieve vulnerabilities for a given host ID asynchronously
    """
    try:
        with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2000)) as session:
            async with session.post(f"https://127.0.0.1/api/cves/{host_id}") as resp:
                data = await resp.json()
            await web.redirect("dashboard")
    except Exception as e:
        # Retry task up to 3 times in case of failure
        raise self.retry(exc=e, countdown=60, max_retries=3)

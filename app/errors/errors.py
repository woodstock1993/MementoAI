from fastapi import HTTPException

def raise_400_url(message):
    raise HTTPException(status_code=400, detail=message)

def raise_url_404(request):
    msg = f"Provided {request.url} does not exist"
    raise HTTPException(status_code=404, detail=msg)

def raise_key_400(request):
    msg = f"Provided key does not exist"
    raise HTTPException(status_code=400, detail=msg)
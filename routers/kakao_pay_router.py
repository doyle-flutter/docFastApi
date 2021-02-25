from typing import Optional
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
import requests

router = APIRouter()

# 결제 요청
@router.get('/')
def kakaopay():
    url = "https://kapi.kakao.com/v1/payment/ready"
    APP_ADMIN_KEY = ""
    headers = {
        "Authorization" : f"KakaoAK {APP_ADMIN_KEY}", 
        "content-type" : "application/x-www-form-urlencoded;charset=utf-8"
    }
    query = f"?cid=TC0ONETIME&partner_order_id=partner_order_id&partner_user_id=partner_user_id&item_name=초코파이&quantity=1&total_amount=2200&vat_amount=200&tax_free_amount=0&approval_url=http://localhost:8000/kakaopay/success&fail_url=http://localhost:8000/kakaopay/fail&cancel_url=http://localhost:8000/kakaopay/cancel"
    _res = requests.post(url= url+query, headers= headers)
    _result = _res.json()
    _next_redirect_pc_url = _result["next_redirect_pc_url"]
    _redirectUrl = RedirectResponse(_next_redirect_pc_url,)
    _redirectUrl.set_cookie(key="ttid",value= str(_result["tid"]))
    return _redirectUrl

# 결제 승인
@router.get('/success')
def kakaopay_success(request: Request, response: Response, pg_token: Optional[str]):
    url = "https://kapi.kakao.com/v1/payment/approve"
    APP_ADMIN_KEY = ""
    headers = {
        "Authorization" : f"KakaoAK {APP_ADMIN_KEY}", 
        "content-type" : "application/x-www-form-urlencoded;charset=utf-8"
    }
    tid = request.cookies.get("ttid")
    query = f"?cid=TC0ONETIME&tid={tid}&partner_order_id=partner_order_id&partner_user_id=partner_user_id&pg_token={pg_token}"
    _res = requests.post(url= url+query, headers= headers)
    _result = _res.json()
    response.set_cookie(key="ttid", value=None)
    return {"code": _result}

# 결제 실패 및 취소
@router.get('/fail')
def kakaopay_fail():
    return
@router.get('/cancel')
def kakaopay_cancel():
    return
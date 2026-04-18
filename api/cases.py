"""
案件管理API路由
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal

from services.case_service import CaseService

router = APIRouter(prefix="/api/cases", tags=["案件管理"])


class CaseCreate(BaseModel):
    case_no: str
    suspect_name: str
    brand: Optional[str] = None
    amount: Optional[float] = None


class CaseUpdate(BaseModel):
    suspect_name: Optional[str] = None
    brand: Optional[str] = None
    amount: Optional[float] = None


@router.get("", response_model=List[dict])
async def list_cases(
    case_no: Optional[str] = Query(None, description="案件编号模糊匹配"),
    suspect_name: Optional[str] = Query(None, description="嫌疑人姓名模糊匹配"),
    brand: Optional[str] = Query(None, description="涉案品牌模糊匹配"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    案件列表查询
    """
    cases = CaseService.list_cases(
        case_no=case_no,
        suspect_name=suspect_name,
        brand=brand,
        limit=limit,
        offset=offset
    )@router.get("", response_model=List[dict])
async def list_cases(
    case_no: Optional[str] = Query(None, description="案件编号模糊匹配"),
    suspect_name: Optional[str] = Query(None, description="嫌疑人姓名模糊匹配"),
    brand: Optional[str] = Query(None, description="涉案品牌模糊匹配"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    案件列表查询 - 真实模拟案例数据（10个）
    """
    mock_cases = [
        {
            "id": 1,
            "case_no": "(2024)京02刑终3号",
            "suspect_name": "阚某某",
            "brand": "大众、奥迪",
            "amount": 900000.0,
            "created_at": "2024-04-01",
            "status": "已结案",
            "title": "阚某某等销售假冒注册商标的商品罪"
        },
        {
            "id": 2,
            "case_no": "(2017)鄂08刑初11号",
            "suspect_name": "豆全喜",
            "brand": "博世、康明斯、潍柴",
            "amount": 59560.0,
            "created_at": "2017-07-20",
            "status": "已结案",
            "title": "豆全喜销售假冒注册商标的商品罪"
        },
        {
            "id": 3,
            "case_no": "(2017)苏04刑终13号",
            "suspect_name": "曹平",
            "brand": "福特、大众、斯柯达、奥迪",
            "amount": 151315.0,
            "created_at": "2017-10-09",
            "status": "已结案",
            "title": "曹平假冒注册商标罪"
        },
        {
            "id": 4,
            "case_no": "(2016)豫01刑初20号",
            "suspect_name": "郭某某、俞某某",
            "brand": "比亚迪",
            "amount": 287767.66,
            "created_at": "2016-03-11",
            "status": "已结案",
            "title": "郭某某、俞某某等销售假冒注册商标的商品罪"
        },
        {
            "id": 5,
            "case_no": "(2016)豫01刑初145号",
            "suspect_name": "侯蕾、王娜",
            "brand": "别克、雪佛兰",
            "amount": 60693.0,
            "created_at": "2016-02-15",
            "status": "已结案",
            "title": "侯蕾、王娜、杜小飞销售假冒注册商标的商品罪"
        },
        {
            "id": 6,
            "case_no": "(2016)黔01刑初20号",
            "suspect_name": "王雪云",
            "brand": "宝马、MINI、现代、起亚",
            "amount": 679769.0,
            "created_at": "2016-12-23",
            "status": "已结案",
            "title": "王雪云销售假冒注册商标的商品罪"
        },
        {
            "id": 7,
            "case_no": "(2014)郑知刑初字第32号",
            "suspect_name": "王XX",
            "brand": "飞利浦、欧普",
            "amount": 764074.0,
            "created_at": "2014-11-19",
            "status": "已结案",
            "title": "王XX销售假冒注册商标的商品罪"
        },
        {
            "id": 8,
            "case_no": "(2014)郑知刑初字第21号",
            "suspect_name": "贾XX",
            "brand": "福耀（FUYAO）",
            "amount": 408390.0,
            "created_at": "2014-11-19",
            "status": "已结案",
            "title": "贾XX销售假冒注册商标的商品罪"
        },
        {
            "id": 9,
            "case_no": "(2014)昆知刑抗字第2号",
            "suspect_name": "李学容、李学江",
            "brand": "本田（Honda）",
            "amount": 394255.0,
            "created_at": "2014-12-04",
            "status": "已结案",
            "title": "李学容、李学江销售假冒注册商标的商品罪"
        },
        {
            "id": 10,
            "case_no": "(2014)郑知刑初字第21号",
            "suspect_name": "贾保连",
            "brand": "福耀（FUYAO）",
            "amount": 408390.0,
            "created_at": "2014-11-19",
            "status": "已结案",
            "title": "贾保连销售假冒注册商标的商品罪"
        }
    ]

    # 筛选逻辑（让前端搜索能正常用）
    def match_case(case):
        if case_no and case_no not in case["case_no"]:
            return False
        if suspect_name and suspect_name not in case["suspect_name"]:
            return False
        if brand and brand not in case["brand"]:
            return False
        return True

    filtered = [c for c in mock_cases if match_case(c)]
    return filtered[offset:offset+limit]
    return cases


@router.get("/{case_id}", response_model=dict)
async def get_case(case_id: int):
    """
    案件详情
    """
    detail = CaseService.get_case_detail(case_id)
    if not detail:
        raise HTTPException(status_code=404, detail="案件不存在")
    return detail


@router.post("", response_model=dict)
async def create_case(case_data: CaseCreate):
    """
    创建案件
    """
    # 检查案件编号是否已存在
    existing = CaseService.get_case_by_no(case_data.case_no)
    if existing:
        raise HTTPException(status_code=400, detail="案件编号已存在")

    case = CaseService.create_case(
        case_no=case_data.case_no,
        suspect_name=case_data.suspect_name,
        brand=case_data.brand,
        amount=Decimal(str(case_data.amount)) if case_data.amount else None
    )
    return CaseService._case_to_dict(case)


@router.put("/{case_id}", response_model=dict)
async def update_case(case_id: int, case_data: CaseUpdate):
    """
    更新案件
    """
    case = CaseService.update_case(
        case_id=case_id,
        suspect_name=case_data.suspect_name,
        brand=case_data.brand,
        amount=Decimal(str(case_data.amount)) if case_data.amount else None
    )
    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")
    return CaseService._case_to_dict(case)


@router.delete("/{case_id}")
async def delete_case(case_id: int):
    """
    删除案件
    """
    success = CaseService.delete_case(case_id)
    if not success:
        raise HTTPException(status_code=404, detail="案件不存在")
    return {"success": True, "message": "案件已删除"}

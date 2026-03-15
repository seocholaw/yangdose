"""양도코리아 입력 데이터 생성 테스트"""

import pytest
from datetime import date
from yangdose.models import 부속토지, 공시지가, 이월과세정보
from yangdose.yangdokorea_input import (
    이월과세_입력, 공시지가_입력, 토지등급_입력, 증여인_취득원인_변환,
)


def _이순인_토지():
    """이순인 사례 (매곡리 155) 토지 데이터."""
    return 부속토지(
        토지번호=1,
        소재지="충청남도 아산시 탕정면 매곡리 155",
        양도가액=189_510_750,
        공시지가=공시지가(양도당시=214_100, 취득당시=7_500),
        토지등급_기준일_현재=115,
        토지등급_기준일_직전=109,
        토지등급_취득당시=109,
        이월과세=이월과세정보(
            증여일=date(2026, 1, 30),
            증여인_취득일=date(1977, 11, 8),
            증여인_취득원인="매매",
        ),
    )


class Test_이월과세_입력:
    """양도코리아 이월과세 팝업 입력 데이터 테스트"""

    def test_증여일(self):
        결과 = 이월과세_입력(_이순인_토지())
        assert 결과["증여일"] == date(2026, 1, 30)

    def test_증여인_취득일(self):
        결과 = 이월과세_입력(_이순인_토지())
        assert 결과["증여인의 취득일"] == date(1977, 11, 8)

    def test_증여인_취득원인_매매_변환(self):
        결과 = 이월과세_입력(_이순인_토지())
        assert 결과["증여인의 취득원인"] == "1.일반취득"

    def test_이월과세_없으면_에러(self):
        토지 = 부속토지(토지번호=1, 소재지="서울", 양도가액=100)
        with pytest.raises(ValueError, match="이월과세 정보가 없는"):
            이월과세_입력(토지)


class Test_증여인_취득원인_변환:

    def test_매매(self):
        assert 증여인_취득원인_변환("매매") == "1.일반취득"

    def test_일반취득(self):
        assert 증여인_취득원인_변환("일반취득") == "1.일반취득"

    def test_상속(self):
        assert 증여인_취득원인_변환("상속") == "2.상속"

    def test_증여(self):
        assert 증여인_취득원인_변환("증여") == "3.증여"

    def test_알수없는_값_에러(self):
        with pytest.raises(ValueError, match="알 수 없는 증여인 취득원인"):
            증여인_취득원인_변환("없는원인")


class Test_공시지가_입력:

    def test_양도당시(self):
        결과 = 공시지가_입력(_이순인_토지())
        assert 결과["양도당시"] == 214_100

    def test_취득당시(self):
        결과 = 공시지가_입력(_이순인_토지())
        assert 결과["취득당시"] == 7_500

    def test_공시지가_없으면_에러(self):
        토지 = 부속토지(토지번호=1, 소재지="서울", 양도가액=100)
        with pytest.raises(ValueError, match="공시지가 정보가 없는"):
            공시지가_입력(토지)


class Test_토지등급_입력:

    def test_이순인_토지등급(self):
        결과 = 토지등급_입력(_이순인_토지())
        assert 결과["현재"] == 115
        assert 결과["직전"] == 109
        assert 결과["취득당시"] == 109

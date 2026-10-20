import unittest
from calculator import calculate_parking_fee

class TestParkingCalculator(unittest.TestCase):
    
    def test_free_period(self):
        # TC-01: 30분까지 무료
        _, fee, _ = calculate_parking_fee("09:00", "09:30", 0)
        self.assertEqual(fee, 0)
        
    def test_rounding_up(self):
        # TC-02: 31분 (30분 무료 + 1분 -> 10분으로 계산)
        _, fee, _ = calculate_parking_fee("09:00", "09:31", 0)
        self.assertEqual(fee, 500)
        
    def test_normal_calculation(self):
        # TC-03: 60분 (30분 무료 + 30분 -> 3*500)
        _, fee, _ = calculate_parking_fee("09:00", "10:00", 0)
        self.assertEqual(fee, 1500)
        
    def test_next_day_automatic(self):
        # TC-04 (Auto): 23:00 -> 01:00 (2시간, 120분)
        # 120 - 30 = 90분 -> 9 * 500 = 4500원
        _, fee, _ = calculate_parking_fee("23:00", "01:00", 0)
        self.assertEqual(fee, 4500)

    def test_manual_extra_day_and_max_fee_increase(self):
        # 요구사항 반영 확인: +1일 누를 때마다 최대치 20,000원씩 증가
        
        # 1. extra_days=0 (기본) -> 최대 20,000원
        # 10시간 주차 시: (600-30)=570분 -> 57*500 = 28,500원 -> 20,000원 제한
        _, fee, _ = calculate_parking_fee("09:00", "19:00", 0)
        self.assertEqual(fee, 20000)

        # 2. extra_days=1 -> 최대 40,000원
        # 10시간 주차 시: 28,500원 -> 40,000원보다 작으므로 28,500원 그대로
        _, fee, _ = calculate_parking_fee("09:00", "19:00", 1)
        self.assertEqual(fee, 28500)

        # 3. extra_days=1인데 요금이 매우 클 경우 (예: 20시간 주차)
        # 20시간 = 1200분 -> (1200-30)=1170분 -> 117*500 = 58,500원 -> 40,000원 제한
        _, fee, _ = calculate_parking_fee("00:00", "20:00", 1)
        self.assertEqual(fee, 40000)

        # 4. extra_days=2 -> 최대 60,000원
        # 20시간 주차 시: 58,500원 -> 60,000원보다 작으므로 58,500원 그대로
        _, fee, _ = calculate_parking_fee("00:00", "20:00", 2)
        self.assertEqual(fee, 58500)

    def test_max_fee_original(self):
        # TC-12: 원래 최대 요금 20,000원 (extra_days=0일 때)
        _, fee, _ = calculate_parking_fee("09:00", "15:00", 0)
        self.assertEqual(fee, 20000)

    def test_duration_string(self):
        # 시간 문자열 검증
        _, _, dur = calculate_parking_fee("09:00", "10:30", 0)
        self.assertEqual(dur, "1시간 30분")
        _, _, dur = calculate_parking_fee("09:00", "09:15", 0)
        self.assertEqual(dur, "15분")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            calculate_parking_fee("9:0", "10:00", 0)
        with self.assertRaises(ValueError):
            calculate_parking_fee("09:00", "10:0", 0)
        with self.assertRaises(ValueError):
            calculate_parking_fee("aa:bb", "10:00", 0)

if __name__ == "__main__":
    # 직접 실행 시 테스트 결과 출력
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingCalculator)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    
    print(f"\n[테스트 결과]")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures) + len(result.errors)}")
    
    if not result.wasSuccessful():
        exit(1)

import unittest
from calculator import calculate_parking_fee

class TestParkingCalculator(unittest.TestCase):
    
    def test_free_period(self):
        # TC-01: 30분까지 무료
        _, fee, _ = calculate_parking_fee("09:00", "09:30", 0)
        self.assertEqual(fee, 0)
        
    def test_rounding_up(self):
        # TC-02: 31분 (30분 무료 + 1분 -> 10분으로 계산)
        _, fee, _ = calculate_parking_fee("09:00", "09:31", 0)
        self.assertEqual(fee, 500)
        
    def test_normal_calculation(self):
        # TC-03: 60분 (30분 무료 + 30분 -> 3*500)
        _, fee, _ = calculate_parking_fee("09:00", "10:00", 0)
        self.assertEqual(fee, 1500)
        
    def test_next_day_automatic(self):
        # TC-04 (Auto): 23:00 -> 01:00 (2시간, 120분)
        # 120 - 30 = 90분 -> 9 * 500 = 4500원
        _, fee, _ = calculate_parking_fee("23:00", "01:00", 0)
        self.assertEqual(fee, 4500)

    def test_manual_extra_day(self):
        # TC-05 (Manual): 23:00 -> 01:00 + 1일 버튼 = 26시간 (1560분)
        # 1560 - 30 = 1530. 153 * 500 = 76500 -> 20000원 (Max)
        _, fee, _ = calculate_parking_fee("23:00", "01:00", 1)
        self.assertEqual(fee, 20000)

    def test_max_fee(self):
        # TC-12: 최대 요금 20,000원
        _, fee, _ = calculate_parking_fee("09:00", "15:00", 0)
        self.assertEqual(fee, 20000)

    def test_duration_string(self):
        # 시간 문자열 검증
        _, _, dur = calculate_parking_fee("09:00", "10:30", 0)
        self.assertEqual(dur, "1시간 30분")
        _, _, dur = calculate_parking_fee("09:00", "09:15", 0)
        self.assertEqual(dur, "15분")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            calculate_parking_fee("9:0", "10:00", 0)
        with self.assertRaises(ValueError):
            calculate_parking_fee("09:00", "10:0", 0)
        with self.assertRaises(ValueError):
            calculate_parking_fee("aa:bb", "10:00", 0)

if __name__ == "__main__":
    # 직접 실행 시 테스트 결과 출력
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingCalculator)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    
    print(f"\n[테스트 결과]")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures) + len(result.errors)}")
    
    if not result.wasSuccessful():
        exit(1)

import unittest
from calculator import calculate_parking_fee

class TestParkingCalculator(unittest.TestCase):
    
    def test_free_period(self):
        # TC-01: 30분까지 무료
        _, fee, _ = calculate_parking_fee("09:00", "09:30", 0)
        self.assertEqual(fee, 0)
        
    def test_rounding_up(self):
        # TC-02: 31분 (30분 무료 + 1분 -> 10분으로 계산)
        _, fee, _ = calculate_parking_fee("09:00", "09:31", 0)
        self.assertEqual(fee, 500)
        
    def test_normal_calculation(self):
        # TC-03: 60분 (30분 무료 + 30분 -> 3*500)
        _, fee, _ = calculate_parking_fee("09:00", "10:00", 0)
        self.assertEqual(fee, 1500)
        
    def test_next_day_button(self):
        # TC-04: 23:00 -> 01:00 (+1일 버튼)
        # 23:00 ~ 01:00 은 2시간 (120분)
        # 120 - 30 = 90분 -> 9 * 500 = 4500원? 
        # 아, 내 TC-04는 7,500원이라고 적었네. 다시 계산해보자.
        # 2시간 = 120분. 120-30 = 90. 90/10 = 9. 9 * 500 = 4500.
        # 어라, 왜 7500원이라고 생각했지? 
        # 2시간은 120분. 30분 빼면 90분. 90/10 = 9. 9 * 500 = 4500.
        # 아, TC-04의 기대값을 수정해야겠구나. (내가 계산 실수를 했다)
        _, fee, _ = calculate_parking_fee("23:00", "01:00", 1) # 1일 버튼 누름
        # 실제로는 diff가 음수면 자동으로 1일이 더해지는데, +1일 버튼을 또 누르면 2일이 됨.
        # 요구사항: "하루 이상 지나는 주차에는 출차 시간이 입차 시간 뒤로 가지 않아도 된다."
        # "출차 입력칸 옆에 +1일 버튼을 만들어 사용하게 한다."
        # 즉, 23:00 -> 01:00 인 경우, 사용자는 버튼을 눌러야 함.
        # 만약 버튼을 안 눌렀다면? 23:00 -> 01:00 이면 diff가 음수이므로 1일이 자동 적용됨.
        # 일단 버튼을 누르는 시나리오로 테스트.
        pass

    def test_manual_extra_day(self):
        # TC-04 (Corrected Logic): 23:00 -> 01:00 (2시간)
        # 만약 23:00 -> 01:00 입력했을 때 자동으로 1일 처리된다면:
        # 120분 -> 4500원.
        _, fee, _ = calculate_parking_fee("23:00", "01:00", 0)
        self.assertEqual(fee, 4500)
        
        # 만약 23:00 -> 01:00 에 +1일 버튼을 한 번 더 누르면 (총 2일 경과):
        # 120 + 1440 = 1560분. 1560 - 30 = 1530. 153 * 500 = 76500 -> 20000.
        _, fee, _ = calculate_parking_fee("23:00", "01:00", 1)
        self.assertEqual(fee, 20000)

    def test_max_fee(self):
        # TC-12: 최대 요금 20,000원
        _, fee, _ = calculate_parking_fee("09:00", "15:00", 0)
        self.assertEqual(fee, 20000)

    def test_duration_string(self):
        # 시간 문자열 검증
        _, _, dur = calculate_parking_fee("09:00", "10:30", 0)
        self.assertEqual(dur, "1시간 30분")
        _, _, dur = calculate_parking_fee("09:00", "09:15", 0)
        self.assertEqual(dur, "15분")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            calculate_parking_fee("9:0", "10:00", 0)

if __name__ == "__main__":
    unittest.main()

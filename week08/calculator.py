from datetime import datetime, timedelta
import math

def calculate_parking_fee(entry_str, exit_str, extra_days=0):
    """
    입차 시각, 출차 시각, 경과 일수를 바탕으로 주차 요금을 계산합니다.
    """
    fmt = "%H:%M"
    
    # 1. 시간 파싱 및 유효성 검사
    if len(entry_str) != 5 or len(exit_str) != 5 or entry_str[2] != ":" or exit_str[2] != ":":
        raise ValueError("시간 형식이 잘못되었습니다. HH:MM 형식을 사용하세요.")

    try:
        entry_time = datetime.strptime(entry_str, fmt)
        exit_time = datetime.strptime(exit_str, fmt)
    except ValueError:
        raise ValueError("시간 값이 유효하지 않습니다. HH:MM 형식을 사용하세요.")

    # 2. 기본 시간 차이 계산
    diff = exit_time - entry_time
    
    # 3. 출차 시간이 입차 시간보다 빠르면 자동으로 하루가 지난 것으로 처리 (예: 23:00 -> 01:00)
    if diff.total_seconds() < 0:
        diff += timedelta(days=1)
    
    # 4. 사용자가 추가로 누른 '+1일' 버튼만큼 날짜를 더함
    total_diff = diff + timedelta(days=extra_days)
    
    total_minutes = int(total_diff.total_seconds() // 60)
    
    # 5. 요금 계산 로직
    # 30분까지 무료, 이후 10분마다 500원 (10분 미만은 올림)
    fee = 0
    if total_minutes > 30:
        billable_minutes = total_minutes - 30
        units = math.ceil(billable_minutes / 10)
        fee = units * 500
        
    # 6. 최대 요금 제한 수정
    # 요구사항: +1일을 누를 때마다 최대치도 20,000원씩 증가
    # 기본(0일 경과) 최대 요금 20,000원
    # 1일 경과 시 40,000원 (즉, 20000 * (1 + extra_days))
    max_fee_limit = 20000 * (1 + extra_days)
    
    if fee > max_fee_limit:
        fee = max_fee_limit
        
    # 7. 주차 시간 문자열 생성
    hours = total_minutes // 60
    mins = total_minutes % 60
    
    if hours > 0:
        duration_str = f"{hours}시간 {mins}분"
    else:
        duration_str = f"{mins}분"
        
    return total_minutes, fee, duration_str

from datetime import datetime, timedelta
import math

def calculate_parking_fee(entry_str, exit_str, extra_days=0):
    """
    입차 시각, 출차 시각, 경과 일수를 바탕으로 주차 요금을 계산합니다.
    
    Args:
        entry_str (str): 입차 시각 "HH:MM"
        exit_str (str): 출차 시각 "HH:MM"
        extra_days (int): 사용자가 클릭한 '+1일' 버튼 횟수
        
    Returns:
        tuple: (total_minutes, fee, duration_str)
    """
    fmt = "%H:%M"
    
    # 1. 시간 파싱 및 유효성 검사
    if len(entry_str) != 5 or len(exit_str) != 5 or entry_str[2] != ":" or exit_str[2] != ":":
        raise ValueError("시간 형식이 잘못되었습니다. HH:MM 형식을 사용하세요.")

    try:
        entry_time = datetime.strptime(entry_str, fmt)
        exit_time = datetime.strptime(exit_str, fmt)
    except ValueError:
        raise ValueError("시간 값이 유효하지 않습니다. HH:MM 형식을 사용하세요.")

    # 2. 기본 시간 차이 계산
    diff = exit_time - entry_time
    
    # 3. 출차 시간이 입차 시간보다 빠르면 자동으로 하루가 지난 것으로 처리 (예: 23:00 -> 01:00)
    if diff.total_seconds() < 0:
        diff += timedelta(days=1)
    
    # 4. 사용자가 추가로 누른 '+1일' 버튼만큼 날짜를 더함
    total_diff = diff + timedelta(days=extra_days)
    
    total_minutes = int(total_diff.total_seconds() // 60)
    
    # 5. 요금 계산 로직
    # 30분까지 무료, 이후 10분마다 500원 (10분 미만은 올림)
    fee = 0
    if total_minutes > 30:
        billable_minutes = total_minutes - 30
        units = math.ceil(billable_minutes / 10)
        fee = units * 500
        
    # 6. 최대 요금 제한 수정
    # 요구사항: +1일을 누를 때마다 최대치도 20,000원씩 증가
    # 기본(0일 경과) 최대 요금 20,000원
    # 1일 경과 시 40,000원 ...
    max_fee_per_day = 20000
    current_max_fee = max_fee_per_day * (1 + extra_days)
    
    if fee > current_max_fee:
        fee = current_max_fee
        
    # 7. 주차 시간 문자열 생성
    hours = total_minutes // 60
    mins = total_minutes % 60
    
    if hours > 0:
        duration_str = f"{hours}시간 {mins}분"
    else:
        duration_str = f"{mins}분"
        
    return total_minutes, fee, duration_str

from datetime import datetime, timedelta
import math

def calculate_parking_fee(entry_str, exit_str, extra_days=0):
    """
    입차 시각, 출차 시각, 경과 일수를 바탕으로 주차 요금을 계산합니다.
    """
    fmt = "%H:%M"
    
    # 1. 시간 파싱 및 유효성 검사
    # 형식이 정확히 HH:MM(5글자)인지 확인
    if len(entry_str) != 5 or len(exit_str) != 5 or entry_str[2] != ":" or exit_str[2] != ":":
        raise ValueError("시간 형식이 잘못되었습니다. HH:MM 형식을 사용하세요.")

    try:
        entry_time = datetime.strptime(entry_str, fmt)
        exit_time = datetime.strptime(exit_str, fmt)
    except ValueError:
        raise ValueError("시간 값이 유효하지 않습니다. HH:MM 형식을 사용하세요.")

    # 2. 기본 시간 차이 계산
    diff = exit_time - entry_time
    
    # 3. 출차 시간이 입차 시간보다 빠르면 자동으로 하루가 지난 것으로 처리 (예: 23:00 -> 01:00)
    if diff.total_seconds() < 0:
        diff += timedelta(days=1)
    
    # 4. 사용자가 추가로 누른 '+1일' 버튼만큼 날짜를 더함
    total_diff = diff + timedelta(days=extra_days)
    
    total_minutes = int(total_diff.total_seconds() // 60)
    
    # 5. 요금 계산 로직
    # 30분까지 무료, 이후 10분마다 500원 (10분 미만은 올림)
    fee = 0
    if total_minutes > 30:
        billable_minutes = total_minutes - 30
        # math.ceil을 사용하여 10분 단위 올림 처리
        units = math.ceil(billable_minutes / 10)
        fee = units * 500
        
    # 6. 하루 최대 요금 20,000원 제한
    if fee > 20000:
        fee = 20000
        
    # 7. 주차 시간 문자열 생성
    hours = total_minutes // 60
    mins = total_minutes % 60
    
    if hours > 0:
        duration_str = f"{hours}시간 {mins}분"
    else:
        duration_str = f"{mins}분"
        
    return total_minutes, fee, duration_str

from datetime import datetime, timedelta
import math

def calculate_parking_fee(entry_str, exit_str, extra_days=0):
    """
    입차 시각, 출차 시각, 경과 일수를 바탕으로 주차 요금을 계산합니다.
    
    Args:
        entry_str (str): 입차 시각 "HH:MM"
        exit_str (str): 출차 시각 "HH:MM"
        extra_days (int): 사용자가 클릭한 '+1일' 버튼 횟수
        
    Returns:
        tuple: (total_minutes, fee, duration_str)
    """
    fmt = "%H:%M"
    
    # 1. 시간 파싱 및 유효성 검사
    try:
        if len(entry_str) != 5 or len(exit_str) != 5:
            raise ValueError
        entry_time = datetime.strptime(entry_str, fmt)
        exit_time = datetime.strptime(exit_str, fmt)
    except ValueError:
        raise ValueError("시간 형식이 잘못되었습니다. HH:MM 형식을 사용하세요.")

    # 2. 기본 시간 차이 계산
    diff = exit_time - entry_time
    
    # 3. 출차 시간이 입차 시간보다 빠르면 자동으로 하루가 지난 것으로 처리 (예: 23:00 -> 01:00)
    if diff.total_seconds() < 0:
        diff += timedelta(days=1)
    
    # 4. 사용자가 추가로 누른 '+1일' 버튼만큼 날짜를 더함
    total_diff = diff + timedelta(days=extra_days)
    
    total_minutes = int(total_diff.total_seconds() // 60)
    
    # 5. 요금 계산 로직
    # 30분까지 무료, 이후 10분마다 500원 (10분 미만은 올림)
    fee = 0
    if total_minutes > 30:
        billable_minutes = total_minutes - 30
        units = math.ceil(billable_minutes / 10)
        fee = units * 500
        
    # 6. 하루 최대 요금 20,000원 제한
    if fee > 20000:
        fee = 20000
        
    # 7. 주차 시간 문자열 생성
    hours = total_minutes // 60
    mins = total_minutes % 60
    
    if hours > 0:
        duration_str = f"{hours}시간 {mins}분"
    else:
        duration_str = f"{mins}분"
        
    return total_minutes, fee, duration_str

from datetime import datetime, timedelta
import math

def calculate_parking_fee(entry_str, exit_str, extra_days=0):
    """
    입차 시각, 출차 시각, 경과 일수를 바탕으로 주차 요금을 계산합니다.
    
    Args:
        entry_str (str): 입차 시각 "HH:MM"
        exit_str (str): 출차 시각 "HH:MM"
        extra_days (int): 경과된 일수 (+1일 버튼 클릭 횟수)
        
    Returns:
        tuple: (total_minutes, fee, duration_str)
            total_minutes: 총 주차 시간 (분)
            fee: 계산된 요금 (원)
            duration_str: 사람이 보기 편한 주차 시간 문자열 (예: "1시간 30분")
    """
    fmt = "%H:%M"
    try:
        entry_time = datetime.strptime(entry_str, fmt)
        exit_time = datetime.strptime(exit_str, fmt)
    except ValueError:
        raise ValueError("시간 형식이 잘못되었습니다. HH:MM 형식을 사용하세요.")

    # 출차 시간이 입차 시간보다 이전인 경우, extra_days가 반영된 것으로 간주하여 날짜를 더함
    # 하지만 사용자가 명시적으로 +1일을 눌렀을 때만 날짜를 더해야 하므로
    # 로직을 다음과 같이 구성:
    # 1. base_diff = exit_time - entry_time
    # 2. 만약 base_diff 가 음수라면 (예: 23:00 -> 01:00), 이는 자동으로 하루가 지난 것으로 볼 수도 있지만
    #    요구사항에 "+1일 버튼을 만들어 사용하게 한다"라고 했으므로, 
    #    버튼을 누른 만큼만 day를 더해준다.
    
    # 기본 차이 계산
    diff = exit_time - entry_time
    
    # 만약 exit_time < entry_time 이면, 기본적으로 다음날로 계산되어야 함 (예: 23:00 ~ 01:00)
    # 이 경우 diff는 음수가 됨.
    if diff.total_seconds() < 0:
        diff += timedelta(days=1)
        
    # 사용자가 추가로 누른 버튼(+1일)만큼 날짜를 더함
    total_diff = diff + timedelta(days=extra_days)
    
    total_minutes = int(total_diff.total_seconds() // 60)
    
    # 요금 계산 로직
    # 30분까지 무료, 이후 10분마다 500원. 10분 미만 올림.
    fee = 0
    if total_minutes > 30:
        billable_minutes = total_minutes - 30
        # 10분 단위 올림 계산: ceil(billable_minutes / 10) * 500
        units = math.ceil(billable_minutes / 10)
        fee = units * 500
        
    # 하루 최대 요금 20,000원
    if fee > 20000:
        fee = 20000
        
    # 주차 시간 문자열 생성
    hours = total_minutes // 60
    mins = total_minutes % 60
    
    if hours > 0:
        duration_str = f"{hours}시간 {mins}분"
    else:
        duration_str = f"{mins}분"
        
    return total_minutes, fee, duration_str

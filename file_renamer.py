import os
import datetime

def get_creation_date(file_path):
    """파일의 생성 날짜를 반환합니다."""
    return os.path.getctime(file_path)

def generate_new_name(file_path, index, num_digits, parent_folder_name):
    """파일의 새 이름을 생성합니다. 번호를 최대 자릿수에 맞춰서 조정합니다."""
    directory, old_name = os.path.split(file_path)
    file_ext = os.path.splitext(old_name)[1]
    
    # 자릿수에 맞춰서 번호를 포맷
    new_index = str(index).zfill(num_digits)
    
    # 새 파일 이름 생성 (상위 폴더 이름을 파일 이름 앞에 붙임)
    new_name = f"{parent_folder_name}_{new_index}{file_ext}"
    
    return os.path.join(directory, new_name)

def rename_files_in_directory(directory_path):
    """주어진 디렉토리에서 파일을 찾아 이름을 변경합니다."""
    files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    if not files:
        print(f"디렉토리 '{directory_path}'에 파일이 없습니다.")
        return False
    
    # 파일들을 생성 날짜 기준으로 정렬
    files.sort(key=get_creation_date)
    
    # 최대 자릿수 계산
    max_index = len(files)
    num_digits = len(str(max_index))  # 번호의 자릿수 결정
    
    # 상위 폴더 이름을 추출합니다
    parent_folder_name = os.path.basename(directory_path)
    
    # 파일 이름을 변경합니다
    for index, file_path in enumerate(files, start=1):
        new_path = generate_new_name(file_path, index, num_digits, parent_folder_name)
        os.rename(file_path, new_path)
        print(f"파일 '{os.path.basename(file_path)}'의 이름이 '{os.path.basename(new_path)}'로 변경되었습니다.")
    
    return True

def rename_files_recursively(base_directory):
    """주어진 디렉토리 및 하위 디렉토리의 모든 파일 이름을 변경합니다."""
    # 최상위 디렉토리에서 파일 이름 변경 시도
    if not rename_files_in_directory(base_directory):
        # 파일이 없는 경우 하위 디렉토리를 탐색
        for subdir, dirs, files in os.walk(base_directory):
            for dir_name in dirs:
                subdir_path = os.path.join(subdir, dir_name)
                if not rename_files_in_directory(subdir_path):
                    print(f"디렉토리 '{subdir_path}'에 파일이 없습니다.")

def main():
    """메인 함수: 사용자로부터 경로를 입력받아 파일 이름을 변경"""
    path = input("파일 이름을 변경할 디렉토리 경로를 입력하세요: ").strip()
    rename_files_recursively(path)

if __name__ == "__main__":
    main()

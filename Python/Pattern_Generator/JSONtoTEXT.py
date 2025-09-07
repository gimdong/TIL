import json

class NANDTextGenerator:
    def __init__(self, json_filepath=None, json_data=None):
        """
        NAND 텍스트 생성기 초기화
        
        Args:
            json_filepath: JSON 파일 경로 (선택사항)
            json_data: JSON 데이터 (선택사항)
        """
        self.json_filepath = json_filepath
        self.json_data = json_data
        self.header_width = 30  # 헤더 라인 총 너비
        
        if json_filepath:
            self.load_json_file(json_filepath)
    
    def load_json_file(self, filepath):
        """JSON 파일 로드"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)
            self.json_filepath = filepath
            print(f"[INFO] JSON 파일이 로드되었습니다: {filepath}")
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON 파일을 찾을 수 없습니다: {filepath}")
        except json.JSONDecodeError:
            raise ValueError(f"유효하지 않은 JSON 파일입니다: {filepath}")
    
    def set_json_data(self, json_data):
        """JSON 데이터 직접 설정"""
        self.json_data = json_data
    
    def set_header_width(self, width):
        """헤더 라인 너비 설정"""
        self.header_width = width
    
    def generate_header_line(self, index, description):
        """
        헤더 라인 생성 (지정된 너비에 맞춰 '-' 개수 자동 조절)
        
        Args:
            index: 인덱스 번호
            description: 설명
            
        Returns:
            str: 포맷된 헤더 라인
        """
        desc = f"*-{index} : {description} "
        dash_count = self.header_width - len(desc)
        if dash_count < 0:
            dash_count = 0
        return desc + '-' * dash_count + '* '
    
    def generate_cmd_line(self, cmd_value):
        """
        CMD 라인 생성
        
        Args:
            cmd_value: CMD 값
            
        Returns:
            str: CMD 라인
        """
        if cmd_value:
            return f"NOP CMD TP<#{cmd_value} TS15"
        return ""
    
    def generate_opt_lines(self, opt_list):
        """
        OPT 라인들 생성
        
        Args:
            opt_list: OPT 리스트
            
        Returns:
            list: OPT 라인들의 리스트
        """
        lines = []
        if isinstance(opt_list, list):
            for opt in opt_list:
                type_ = opt.get('TYPE', '')
                value = opt.get('VALUE', '')
                if type_ and value:
                    lines.append(f"NOP {type_} TP<#{value} TS15")
                elif type_:
                    lines.append(f"NOP {type_} TS15")
        return lines
    
    def generate_item_text(self, item):
        """
        단일 아이템에 대한 텍스트 생성
        
        Args:
            item: JSON 데이터의 단일 아이템
            
        Returns:
            list: 텍스트 라인들의 리스트
        """
        lines = []
        
        # 헤더 라인
        index = item.get('index', '')
        description = item.get('DESCRIPTION', '')
        header = self.generate_header_line(index, description)
        lines.append(header)
        
        # CMD 라인
        cmd = item.get('CMD', '')
        cmd_line = self.generate_cmd_line(cmd)
        if cmd_line:
            lines.append(cmd_line)
        
        # OPT 라인들
        opt_list = item.get('OPT', [])
        opt_lines = self.generate_opt_lines(opt_list)
        lines.extend(opt_lines)
        
        return lines
    
    def generate_all_text(self):
        """
        전체 텍스트 생성
        
        Returns:
            list: 모든 텍스트 라인들의 리스트
        """
        if not self.json_data:
            raise ValueError("JSON 데이터가 설정되지 않았습니다.")
        
        all_lines = []
        for item in self.json_data:
            item_lines = self.generate_item_text(item)
            all_lines.extend(item_lines)
            # 각 아이템 사이에 빈 줄 추가하지 않음 (원본 코드와 동일)
        
        return all_lines
    
    def save_to_text_file(self, output_filepath, lines=None):
        """
        텍스트 파일로 저장
        
        Args:
            output_filepath: 출력 파일 경로
            lines: 저장할 라인들 (None이면 전체 텍스트 생성)
        """
        if lines is None:
            lines = self.generate_all_text()
        
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n')
            
            print(f"[INFO] 텍스트 파일로 저장되었습니다: {output_filepath}")
        except Exception as e:
            raise IOError(f"파일 저장 중 오류 발생: {e}")
    
    def generate_and_save(self, output_filepath):
        """
        텍스트 생성 및 저장을 한 번에 수행
        
        Args:
            output_filepath: 출력 파일 경로
            
        Returns:
            list: 생성된 텍스트 라인들
        """
        lines = self.generate_all_text()
        self.save_to_text_file(output_filepath, lines)
        return lines
    
    def preview_text(self, num_items=5):
        """
        생성될 텍스트 미리보기
        
        Args:
            num_items: 미리볼 아이템 개수
        """
        if not self.json_data:
            raise ValueError("JSON 데이터가 설정되지 않았습니다.")
        
        preview_data = self.json_data[:num_items]
        lines = []
        for item in preview_data:
            item_lines = self.generate_item_text(item)
            lines.extend(item_lines)
        
        print("=== 텍스트 미리보기 ===")
        for line in lines:
            print(line)
        print("=" * 25)

# 사용 예시:
# generator = NANDTextGenerator('./WL_01_ver01.json')
# generator.generate_and_save('./WL_01.txt')
# 
# # 또는
# generator = NANDTextGenerator()
# generator.load_json_file('./WL_01_ver01.json')
# generator.set_header_width(35)  # 헤더 너비 변경
# generator.preview_text(3)  # 미리보기
# generator.generate_and_save('./WL_01.txt')
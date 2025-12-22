# 脚本1：html_error_cleaner.py
from bs4 import BeautifulSoup
import os

def process_html_with_error_extraction(input_html_path, output_html_path, error_txt_path="error项.txt"):
    # 1. 读取输入HTML文件
    if not os.path.exists(input_html_path):
        raise FileNotFoundError(f"输入文件不存在：{input_html_path}")
    
    with open(input_html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 2. 解析HTML，按层级定位：html → body[onload="init()"] → table[id="result-table"] → tbody
    soup = BeautifulSoup(html_content, "lxml")
    
    # 定位body（带onload="init()"属性）
    target_body = soup.find("body", attrs={"onload": "init()"})
    if not target_body:
        raise ValueError("未找到符合条件的body标签（onload=\"init()\"）")
    
    # 定位表格（id="result-table"）
    target_table = target_body.find("table", id="result-table")
    if not target_table:
        raise ValueError("未找到符合条件的表格（id=\"result-table\"）")
    
    # 定位所有tbody标签
    all_tbodies = target_table.find_all("tbody")
    if not all_tbodies:
        print("未找到任何tbody标签，无需处理")
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        return

    # 3. 筛选并处理error类tbody，提取td文本
    error_td_texts = []
    for tbody in all_tbodies:
        # 判断tbody的class是否包含"error result-table-row"（支持多class场景）
        tbody_classes = tbody.get("class", [])
        target_class = "error result-table-row"
        # 兼容class是字符串（单个class）或列表（多个class）的情况
        if (isinstance(tbody_classes, str) and target_class in tbody_classes) or \
           (isinstance(tbody_classes, list) and all(c in tbody_classes for c in target_class.split())):
            
            # 提取该tbody下<tr>中的<td class="col-name">文本
            tr_tags = tbody.find_all("tr")
            for tr in tr_tags:
                td_col_name = tr.find("td", class_="col-name")
                if td_col_name:
                    td_text = td_col_name.get_text(strip=True)
                    if td_text:  # 过滤空文本
                        error_td_texts.append(td_text)
            
            # 删除该tbody标签
            tbody.decompose()

    # 4. 保存处理后的HTML文件
    with open(output_html_path, "w", encoding="utf-8") as f:
        # prettify()保证HTML格式整洁，便于阅读
        f.write(soup.prettify())
    print(f"处理后的HTML已保存至：{output_html_path}")

    # 5. 保存error项txt文件
    with open(error_txt_path, "w", encoding="utf-8") as f:
        for idx, text in enumerate(error_td_texts, 1):
            f.write(f"{idx}. {text}\n")
    print(f"Error项文本已保存至：{error_txt_path}")
    print(f"共提取到 {len(error_td_texts)} 个error项")

if __name__ == "__main__":
    # 配置文件路径（可根据实际需求修改）
    INPUT_HTML = "input.html"       # 原始HTML文件
    OUTPUT_HTML = "output_cleaned.html"  # 处理后的HTML文件
    ERROR_TXT = "error项.txt"        # 输出的error项文本文件

    try:
        process_html_with_error_extraction(INPUT_HTML, OUTPUT_HTML, ERROR_TXT)
    except Exception as e:
        print(f"执行出错：{e}")

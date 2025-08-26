#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预设实验模板 - 支持命令行参数和预设实验配置

用法:
  python preset_experiments_template.py                    # 运行预设实验
  python preset_experiments_template.py --help            # 查看帮助
  python preset_experiments_template.py --input data --param1 value  # 自定义参数
"""

import sys
import argparse
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    """实验配置类"""
    experiment_name: str = "默认实验"
    input_path: str = "data" # 当前开发/实验/测试下的data目录
    output_path: str = "results" # 当前开发/实验/测试下的results目录
    param1: str = "默认参数"
    param2: int = 100
    param3: bool = False
    param4: List[str] = field(default_factory=lambda: ["item1", "item2"])


def run_experiment(config: Config) -> bool:
    """运行单个实验"""
    try:
        print(f"\n=== 开始运行实验: {config.experiment_name} ===")
        print(f"输入路径: {config.input_path}")
        print(f"输出路径: {config.output_path}")
        print(f"参数1: {config.param1}")
        print(f"参数2: {config.param2}")
        print(f"参数3: {config.param3}")
        print(f"参数4: {config.param4}")

        # 运行实验
        # 可以是直接在同一个文件中写代码，也可以是调用其他函数或模块
        
        print(f"=== 实验 {config.experiment_name} 运行完成 ===")
        return True
    except Exception as e:
        print(f"实验 {config.experiment_name} 运行失败: {str(e)}")
        return False


def parse_arguments() -> Config:
    """解析命令行参数并返回 Config 实例"""
    parser = argparse.ArgumentParser(description="预设实验模板", epilog="""
示例:
  python preset_experiments_template.py
  python preset_experiments_template.py --input data --param1 value --param2 300
  python preset_experiments_template.py --param3 --param4 item1 item2 item3
    """)
    
    parser.add_argument('--input', '-i', help='输入路径')
    parser.add_argument('--output', '-o', help='输出路径')
    parser.add_argument('--name', '-n', help='实验名称')
    parser.add_argument('--param1', help='参数1')
    parser.add_argument('--param2', type=int, help='参数2')
    parser.add_argument('--param3', action='store_true', help='参数3 (布尔值)')
    parser.add_argument('--param4', nargs='*', help='参数4 (列表)')
    
    args = parser.parse_args()
    config = Config()
    config.experiment_name = "命令行实验"
    config.input_path = args.input
    config.output_path = args.output
    config.param1 = args.param1
    config.param2 = args.param2
    config.param3 = args.param3
    config.param4 = args.param4
    return config


def run_from_args():
    """从命令行参数运行实验"""
    # 解析命令行参数
    config = parse_arguments()
    
    # 运行实验
    print("开始运行命令行实验...")
    success = run_experiment(config)
    print(f"命令行实验运行{'成功' if success else '失败'}")


def preset_experiment_1():
    return Config(experiment_name="实验 1", param1="实验1参数", param2=200, param3=True)


def preset_experiment_2():
    return Config(experiment_name="实验 2", input_path="./test_data", output_path="./test_results", 
               param1="实验2参数", param2=300, param4=["test1", "test2", "test3"])


def run_preset_experiments():
    """运行所有预设实验"""
    # 预设实验列表
    preset_experiments = [
        preset_experiment_1(),
        preset_experiment_2()
    ]
    
    print("开始运行预设实验...")
    for i, config in enumerate(preset_experiments, 1):
        print(f"\n--- 准备运行第 {i} 个实验 ---")
        success = run_experiment(config)
        print(f"第 {i} 个实验运行{'成功' if success else '失败'}") 
    print("\n所有预设实验运行完成")


def main():
    """主函数"""
    # 判断是从命令行运行还是从预设实验列表运行
    if len(sys.argv) > 1:
        # 有参数
        run_from_args()  # 从命令行运行  
    else:  
        # 无参数
        run_preset_experiments()  # 从预设实验列表运行


if __name__ == '__main__':
    main() 
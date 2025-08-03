#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预设实验模板
用于快速设置和运行不同配置的实验

使用方法:
1. 运行所有预设实验:
   python preset_experiments_template.py

2. 从命令行参数直接配置和运行实验:
   python preset_experiments_template.py input_path output_path param1 200
   # 参数顺序: [输入路径] [输出路径] [参数1] [参数2]
   # 完全不走预设实验路径，直接根据命令行参数配置
"""

import sys
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Config:
    """配置类 - 根据具体需求自定义字段"""
    # 基础配置
    experiment_name: str = "默认实验"
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    
    # 示例配置字段（根据实际需求修改）
    param1: str = "默认值1"
    param2: int = 100
    param3: bool = False
    param4: List[str] = None
    
    def __post_init__(self):
        """初始化后的验证和设置"""
        if self.param4 is None:
            self.param4 = []


def run_experiment(config: Config) -> bool:
    """
    运行单个实验
    
    Args:
        config: 实验配置
        
    Returns:
        bool: 实验是否成功
    """
    try:
        print(f"\n=== 开始运行实验: {config.experiment_name} ===")
        print(f"输入路径: {config.input_path}")
        print(f"输出路径: {config.output_path}")
        print(f"参数1: {config.param1}")
        print(f"参数2: {config.param2}")
        print(f"参数3: {config.param3}")
        print(f"参数4: {config.param4}")
        
        # TODO: 在这里添加具体的实验逻辑
        # 例如：
        # - 数据处理
        # - 模型训练
        # - 结果分析
        # - 文件操作
        # - API调用
        # - 等等
        
        print(f"=== 实验 {config.experiment_name} 运行完成 ===")
        return True
        
    except Exception as e:
        print(f"实验 {config.experiment_name} 运行失败: {str(e)}")
        return False


def default_config() -> Config:
    """默认配置"""
    return Config(
        experiment_name="默认实验",
        input_path="./data",
        output_path="./results",
        param1="默认参数",
        param2=100,
        param3=False,
        param4=["item1", "item2"]
    )


def preset_experiment_1() -> Config:
    """预设实验 1"""
    config = default_config()
    config.experiment_name = "实验 1"
    config.param1 = "实验1参数"
    config.param2 = 200
    config.param3 = True
    return config


def preset_experiment_2() -> Config:
    """预设实验 2"""
    config = default_config()
    config.experiment_name = "实验 2"
    config.input_path = "./test_data"
    config.output_path = "./test_results"
    config.param1 = "实验2参数"
    config.param2 = 300
    config.param4 = ["test1", "test2", "test3"]
    return config


def preset_experiment_3() -> Config:
    """预设实验 3"""
    config = default_config()
    config.experiment_name = "实验 3"
    config.param1 = "实验3参数"
    config.param2 = 500
    config.param3 = True
    config.param4 = ["exp3_item1", "exp3_item2"]
    return config


def run_all_preset_experiments():
    """运行所有预设实验"""
    # 定义所有预设实验函数
    experiments = [
        preset_experiment_1,
        preset_experiment_2,
        preset_experiment_3,
    ]
    
    print("开始运行预设实验...")
    
    # 连续运行所有实验
    for i, experiment_func in enumerate(experiments, 1):
        print(f"\n--- 准备运行第 {i} 个实验 ---")
        
        # 获取实验配置
        config = experiment_func()
        
        # 运行实验
        success = run_experiment(config)
        
        if success:
            print(f"第 {i} 个实验运行成功")
        else:
            print(f"第 {i} 个实验运行失败，继续下一个实验")
    
    print("\n所有预设实验运行完成")


def run_from_command_line(args: list) -> bool:
    """
    从命令行参数直接配置和运行实验
    
    Args:
        args: 命令行参数列表
        
    Returns:
        bool: 实验是否成功运行
    """
    print("从命令行参数配置实验...")
    
    # 创建默认配置
    config = default_config()
    
    # 根据命令行参数动态配置实验
    # 这里可以根据实际需求解析命令行参数
    # 例如：--input, --output, --param1, --param2 等
    
    # 示例：简单的参数解析
    if len(args) > 1:
        config.experiment_name = f"命令行实验: {args[1]}"
        config.input_path = args[1] if len(args) > 1 else config.input_path
        config.output_path = args[2] if len(args) > 2 else config.output_path
        config.param1 = args[3] if len(args) > 3 else config.param1
        config.param2 = int(args[4]) if len(args) > 4 and args[4].isdigit() else config.param2
    
    print(f"命令行配置完成: {config.experiment_name}")
    return run_experiment(config)


def main():
    """主函数 - 根据是否有命令行参数决定运行模式"""
    if len(sys.argv) > 1:
        # 有命令行参数：完全不走预设实验路径，直接根据命令行参数配置和运行
        success = run_from_command_line(sys.argv)
        if not success:
            sys.exit(1)  # 实验失败时退出码为1
    else:
        # 无命令行参数：运行所有预设实验
        run_all_preset_experiments()


if __name__ == '__main__':
    main() 
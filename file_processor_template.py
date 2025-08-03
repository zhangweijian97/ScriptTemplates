#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件处理脚本模板
用于处理各种文件操作的基础模板
"""

import os
import sys
import argparse
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict


class ProcessingStrategy:
    """处理策略类，控制文件处理结果的保存方式"""
    
    def __init__(self, save_individual: bool = True, save_summary: bool = False):
        """
        初始化处理策略
        
        Args:
            save_individual: 是否保存单个文件处理结果
            save_summary: 是否保存汇总结果
        """
        self.save_individual = save_individual
        self.save_summary = save_summary
        
    def __str__(self):
        return f"ProcessingStrategy(save_individual={self.save_individual}, save_summary={self.save_summary})"


@dataclass
class Config:
    """配置类"""
    input: Optional[str] = None  # 输入路径，将在运行时设置
    log_level: str = 'INFO'
    file_extensions: Optional[List[str]] = None
    output_dir: str = './output'
    save_mode: str = 'individual'  # 'individual', 'summary', 'both'
    
    def __post_init__(self):
        """验证配置"""
        if self.file_extensions is None:
            self.file_extensions = []

class FileProcessor:
    """文件处理器类"""
    
    def __init__(self, config: Config, strategy: ProcessingStrategy = None):
        """
        初始化文件处理器
        
        Args:
            config: 配置对象
            strategy: 处理策略，控制结果保存方式
        """
        self.config = config
        self.strategy = strategy or ProcessingStrategy()
        self.setup_logging()
        
    def setup_logging(self):
        log_level = self.config.log_level
        # 只在第一次设置日志配置
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=getattr(logging, log_level),
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
        self.logger = logging.getLogger(__name__)
        
    def _do_process(self, file_path: str) -> Dict[str, Any]:
        """
        执行具体的文件处理逻辑
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        # TODO: 在这里添加具体的文件处理逻辑
        # 例如：读取文件内容、转换格式、分析数据等
        
        # 示例：返回文件的基本信息（仅作演示，实际使用时请替换）
        path = Path(file_path)
        result = {
            'file_path': str(file_path),
            'status': 'success'
        }
        
        return result
        
    def _save_individual_result(self, result: Dict[str, Any]):
        """
        保存单个文件的处理结果
        
        Args:
            result: 处理结果，包含文件路径等信息
        """
        # 验证数据完整性
        if 'file_path' not in result:
            self.logger.error("结果中缺少 file_path 字段")
            return
            
        # TODO: 开发者根据需求实现保存逻辑
        # 可以保存为任意格式、任意数量的文件
        # 示例：
        # - 保存为 JSON、CSV、TXT 等格式
        # - 保存到指定目录
        # - 生成带时间戳的文件名
        # - 处理文件编码问题
        # - 根据处理结果动态生成文件名
        pass
            
    def _save_summary_results(self, results: Dict[str, Any]):
        """
        保存汇总结果
        
        Args:
            results: 目录处理结果，包含目录信息和所有文件结果
        """
        # TODO: 开发者根据需求实现保存逻辑
        # 可以保存为任意格式、任意数量的文件
        # 示例：
        # - 保存为 JSON 格式的详细结果
        # - 保存为 CSV 格式的统计摘要
        # - 保存为 TXT 格式的日志报告
        # - 保存为 HTML 格式的可视化报告
        # - 根据处理结果动态生成文件名
        # - 保存多个不同格式的文件
        pass
        
    def _format_time(self, seconds: float) -> str:
        """
        格式化时间显示
        
        Args:
            seconds: 秒数
            
        Returns:
            str: 格式化的时间字符串
        """
        if seconds < 1:
            milliseconds = int(seconds * 1000)
            return f"{milliseconds}毫秒"
        elif seconds < 60:
            return f"{seconds:.2f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.2f}小时"
        
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        处理单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 处理结果，包含文件信息、处理信息和结果信息
        """
        try:
            path = Path(file_path)
            if not path.exists():
                self.logger.error(f"文件不存在: {file_path}")
                return {
                    'file_path': str(file_path),
                    'status': 'failed',
                    'error': '文件不存在',
                    'process_time': 0
                }
                
            self.logger.info(f"开始处理文件: {file_path}")
            
            # 记录开始时间
            start_time = time.time()
            
            # 执行具体的处理逻辑
            result = self._do_process(file_path)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 添加处理时间到结果中
            result['process_time'] = round(process_time, 3)
            
            # 根据策略决定是否保存单个结果
            if self.strategy.save_individual:
                self._save_individual_result(result)
            
            self.logger.info(f"文件处理完成: {file_path} (耗时: {self._format_time(process_time)})")
            return result
            
        except Exception as e:
            self.logger.error(f"处理文件时出错 {file_path}: {str(e)}")
            # 记录失败的结果
            failed_result = {
                'file_path': file_path,
                'status': 'failed',
                'error': str(e),
                'process_time': 0
            }
            return failed_result
    
    def process_directory(self, dir_path: str) -> Dict[str, Any]:
        """
        处理目录中的所有文件
        
        Args:
            dir_path: 目录路径
            
        Returns:
            Dict[str, Any]: 目录处理结果，包含目录信息、处理信息和所有文件结果
        """
        path = Path(dir_path)
        
        if not path.exists():
            self.logger.error(f"目录不存在: {dir_path}")
            return {
                'file_dir': str(dir_path),
                'status': 'failed',
                'error': '目录不存在',
                'file_count': 0,
                'process_time': 0,
                'results': []
            }
            
        if not path.is_dir():
            self.logger.error(f"路径不是目录: {dir_path}")
            return {
                'file_dir': str(dir_path),
                'status': 'failed',
                'error': '路径不是目录',
                'file_count': 0,
                'process_time': 0,
                'results': []
            }
            
        # 记录开始时间
        start_time = time.time()
        self.logger.info(f"开始处理目录: {dir_path}")
        
        # 获取文件扩展名过滤条件
        extensions = self.config.file_extensions
        
        # 收集所有文件路径
        file_paths = []
        for file_path in path.rglob('*'):
            if file_path.is_file():
                # 检查文件扩展名
                if extensions and file_path.suffix.lower() not in extensions:
                    continue
                file_paths.append(str(file_path))
        
        # 处理所有文件
        file_results = []
        for file_path in file_paths:
            result = self.process_file(file_path)
            file_results.append(result)
        
        # 计算处理时间
        total_time = time.time() - start_time
        
        # 统计成功和失败的文件数
        success_count = sum(1 for result in file_results if result.get('status') == 'success')
        failed_count = len(file_results) - success_count
        
        # 构建目录处理结果
        results = {
            'file_dir': str(dir_path),
            'file_count': len(file_results),
            'success_count': success_count,
            'failed_count': failed_count,
            'process_time': round(total_time, 3),
            'average_time': round(total_time / len(file_results), 3) if file_results else 0,
            'status': 'success' if failed_count == 0 else 'partial_success',
            'results': file_results
        }
        
        # 如果策略要求保存汇总结果，则保存
        if self.strategy.save_summary:
            self._save_summary_results(results)
        
        self.logger.info(f"目录处理完成: {dir_path} (总耗时: {self._format_time(total_time)})")
        return results


def load_config(config_path: Optional[str] = None) -> Config:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        Config: 配置对象
    """
    # 创建默认配置
    config = Config()
    
    # TODO: 如果提供了配置文件路径，在这里加载配置文件
    # 可以使用 JSON、YAML 或其他格式
    # 示例：
    # if config_path and Path(config_path).exists():
    #     with open(config_path, 'r', encoding='utf-8') as f:
    #         config_data = json.load(f)
    #         # 更新配置对象
    #         for key, value in config_data.items():
    #             if hasattr(config, key):
    #                 setattr(config, key, value)
    
    return config


def create_strategy_from_config(config: Config) -> ProcessingStrategy:
    """
    根据配置创建处理策略
    
    Args:
        config: 配置对象
        
    Returns:
        ProcessingStrategy: 处理策略对象
    """
    save_mode = config.save_mode
    
    if save_mode == 'individual':
        return ProcessingStrategy(save_individual=True, save_summary=False)
    elif save_mode == 'summary':
        return ProcessingStrategy(save_individual=False, save_summary=True)
    elif save_mode == 'both':
        return ProcessingStrategy(save_individual=True, save_summary=True)
    else:
        # 默认策略
        return ProcessingStrategy(save_individual=True, save_summary=False)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='文件处理脚本模板')
    parser.add_argument('input', help='输入文件或目录路径')
    parser.add_argument('-c', '--config', help='配置文件路径')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('--save-mode', choices=['individual', 'summary', 'both'], 
                       help='保存模式：individual(单个文件), summary(汇总), both(两者都保存)')
    
    return parser.parse_args()


def main(config: Config):
    """主函数"""
    try:
        # 验证输入路径
        if not config.input or not config.input.strip():
            print("错误：未设置输入路径或输入路径为空")
            return False
        
        # 创建处理策略
        strategy = create_strategy_from_config(config)
        
        # 创建文件处理器
        processor = FileProcessor(config, strategy)
        
        # 处理输入路径
        input_path = Path(config.input)
        
        if input_path.is_file():
            # 处理单个文件
            result = processor.process_file(str(input_path))
            if result.get('status') == 'success':
                print(f"文件处理成功: {input_path}")
                print(f"处理时间: {processor._format_time(result['process_time'])}")
            else:
                print(f"文件处理失败: {input_path}")
                print(f"错误信息: {result.get('error', '未知错误')}")
                
        elif input_path.is_dir():
            # 处理目录
            results = processor.process_directory(str(input_path))
            
            if results.get('status') == 'success':
                print(f"目录处理成功: {input_path}")
            elif results.get('status') == 'partial_success':
                print(f"目录处理部分成功: {input_path}")
            else:
                print(f"目录处理失败: {input_path}")
                print(f"错误信息: {results.get('error', '未知错误')}")
            
            print(f"文件统计: {results['success_count']}/{results['file_count']} 个文件成功")
            print(f"处理时间: {processor._format_time(results['process_time'])}")
            print(f"平均时间: {processor._format_time(results['average_time'])}")
            print(f"使用策略: {strategy}")
        return True
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        return False

def run_from_cmd():
    args = parse_arguments()
    
    # 加载配置
    config = load_config(args.config)
    
    # 更新配置
    config.input = args.input  # 将input添加到config中
    if args.output:
        config.output_dir = args.output
    if args.verbose:
        config.log_level = 'DEBUG'
    if args.save_mode:
        config.save_mode = args.save_mode
    
    return main(config)

def preset_experiment_example():
    # 实验示例
    config = Config(
        input='./test_files',
        log_level='DEBUG',
        file_extensions=['.txt'],
        output_dir='./output',
        save_mode='summary'
    )
    return config

def preset_exp_1():
    # 实验 1
    # 根据需要，设置实验参数
    config = Config(
        input='./test_files',
    )
    return config

def preset_exp_2():
    # 实验 2
    config = Config(
        input='./test_files',
    )
    return config

def run_from_preset():
    # 使用预设配置
    experiments = [
        # preset_experiment_example,
        preset_exp_1,
        preset_exp_2,
    ]
    # 可连续运行多个预设实验
    for i, experiment in enumerate(experiments):
        print(f"\n=== 运行实验 {i} ===")
        success = main(experiment())
        if not success:
            print(f"实验 {i} 失败，继续下一个实验")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_from_cmd()
    else:
        run_from_preset()

import json
import os
from typing import Dict, Any

class ConfigManager:
    """配置管理器，用于保存和加载应用配置"""
    
    def __init__(self, config_file: str = 'email_config.json'):
        self.config_file = config_file
    
    def save_email_config(self, config: Dict[str, Any]) -> bool:
        """
        保存邮件配置到文件
        
        Args:
            config: 配置字典
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保配置目录存在
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            # 保存配置到文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"保存配置失败: {str(e)}")
            return False
    
    def load_email_config(self) -> Dict[str, Any]:
        """
        从文件加载邮件配置
        
        Returns:
            Dict[str, Any]: 配置字典
        """
        default_config = {
            'SMTP_SERVER': 'smtp.163.com',  # 163邮箱SMTP服务器
            'SMTP_PORT': 25,                # 163邮箱端口
            'SMTP_USERNAME': '',
            'SMTP_PASSWORD': '',
            'EMAIL_FROM': '',
            'EMAIL_FROM_NAME': 'AnswerCustomer System',
            'SMTP_USE_TLS': False           # 163邮箱不使用TLS
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置，确保所有字段都存在
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                return default_config
        except Exception as e:
            print(f"加载配置失败: {str(e)}")
            return default_config
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        更新配置
        
        Args:
            updates: 要更新的配置项
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 加载当前配置
            current_config = self.load_email_config()
            
            # 更新配置
            current_config.update(updates)
            
            # 保存更新后的配置
            return self.save_email_config(current_config)
        except Exception as e:
            print(f"更新配置失败: {str(e)}")
            return False 
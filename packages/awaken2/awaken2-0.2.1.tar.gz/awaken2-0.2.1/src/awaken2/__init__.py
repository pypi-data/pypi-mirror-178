# Copyright 2022 quinn.7@foxmail.com All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" 
[ 关键字驱动自动化框架 ]

Awaken 是以 "关键字驱动" 为中心思想搭建的自动化测试框架。
其核心实现是通过相比编程语言更加语义化的 "关键字" 来组织自动化用例的逻辑实现;
相较于传统的通过编程语言直接编写的自动化脚本而言, "关键字驱动" 极大降低了技术栈的门槛, 使得非技术人员也能参与其中;
但这种 "便捷" 的代价便是牺牲了原生编码的部分灵活性, 并且将功能实现的职责嫁接给框架开发者。

"""


# --------------------------------------------------------------------------
class AwakenDetails:
    """ 
    [ Awaken详情结构体 ] 
    
    """
    Name     = 'awaken2'
    """ 项目名称 """
    Version  = '0.2.1'
    """ 项目版本 """
    Desc     = 'Awaken 是以 "关键字驱动" 为中心思想搭建的自动化测试框架。'
    """ 项目简介 """
    Url      = 'https://gitee.com/catcat7/awaken2'
    """ 项目URL """
    Author   = 'chenjiancheng'
    """ 项目作者 """
    Email    = 'quinn.7@foxmail.com'
    """ 作者邮箱 """
    Keywords = ['python', 'testing', 'automation', 'testautomation', 'awaken2']
    """ 项目关键字 """

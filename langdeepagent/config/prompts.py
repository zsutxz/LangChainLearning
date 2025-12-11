"""
英语学习提示词模板
"""

# 英语水平评估提示词
LEVEL_ASSESSMENT_PROMPT = """
作为专业的英语教师，请根据用户的信息评估英语水平：

用户当前自评水平：{current_level}
学习目标：{learning_goals}
目标场景：{target_scenario}

请提供详细的水平评估，包括：
1. 当前水平的详细描述（词汇量、语法掌握程度、听说读写能力）
2. 优势领域分析
3. 需要改进的方面
4. 具体的能力评分（1-10分）
5. 学习建议和重点

请返回JSON格式的评估结果：
{{
    "current_level": "详细水平描述",
    "vocabulary_level": 评分,
    "grammar_level": 评分,
    "listening_level": 评分,
    "speaking_level": 评分,
    "reading_level": 评分,
    "writing_level": 评分,
    "strengths": ["优势1", "优势2"],
    "weaknesses": ["弱项1", "弱项2"],
    "recommendations": ["建议1", "建议2"]
}}
"""

# 学习计划生成提示词
LEARNING_PLAN_PROMPT = """
作为英语学习专家，请为用户制定个性化学习计划：

用户信息：
- 当前水平：{current_level}
- 学习目标：{learning_goals}
- 目标场景：{target_scenario}
- 可用学习时间：{study_time} 小时/天
- 学习期限：{duration} 周

请制定详细的学习计划，包括：
1. 总体学习目标和里程碑
2. 每周学习重点
3. 词汇学习计划
4. 语法学习路径
5. 听说读写训练安排
6. 学习资源和材料推荐
7. 进度评估方法

返回JSON格式的学习计划：
{{
    "overall_goals": ["目标1", "目标2"],
    "milestones": [
        {{
            "week": 1,
            "goals": ["周目标1", "周目标2"],
            "vocabulary_focus": "词汇重点",
            "grammar_focus": "语法重点",
            "practice_activities": ["活动1", "活动2"]
        }}
    ],
    "daily_schedule": {{
        "vocabulary": "词汇学习安排",
        "grammar": "语法学习安排",
        "listening": "听力练习安排",
        "speaking": "口语练习安排",
        "reading": "阅读练习安排",
        "writing": "写作练习安排"
    }},
    "resources": {{
        "textbooks": ["教材1", "教材2"],
        "websites": ["网站1", "网站2"],
        "apps": ["应用1", "应用2"],
        "videos": ["视频1", "视频2"]
    }}
}}
"""

# 词汇学习提示词
VOCABULARY_LEARNING_PROMPT = """
作为词汇专家，请为用户制定词汇学习计划：

用户水平：{current_level}
学习主题：{topic}
需学词汇数量：{count}
目标场景：{target_scenario}

请提供：
1. 核心词汇列表（包含词性、词义、例句）
2. 词汇分类和组织方法
3. 记忆技巧和学习策略
4. 词汇运用练习
5. 复习计划安排

返回JSON格式：
{{
    "vocabulary_list": [
        {{
            "word": "单词",
            "phonetic": "音标",
            "part_of_speech": "词性",
            "definition": "词义",
            "example_sentence": "例句",
            "synonyms": ["同义词1", "同义词2"],
            "antonyms": ["反义词1", "反义词2"],
            "memory_tips": "记忆技巧",
            "difficulty": "难度等级"
        }}
    ],
    "learning_strategies": ["策略1", "策略2"],
    "practice_exercises": [
        {{
            "type": "练习类型",
            "content": "练习内容",
            "answer": "答案"
        }}
    ],
    "review_schedule": "复习计划"
}}
"""

# 对话练习提示词
CONVERSATION_PRACTICE_PROMPT = """
作为英语口语教练，请设计对话练习场景：

场景：{scenario}
难度级别：{difficulty_level}
用户水平：{current_level}
学习目标：{learning_goals}

请创建：
1. 场景背景介绍
2. 对话角色设定
3. 对话流程和脚本
4. 关键表达和句型
5. 文化注意事项
6. 常见问题和回答

返回JSON格式：
{{
    "scenario": "场景描述",
    "background": "背景介绍",
    "roles": [
        {{
            "name": "角色名",
            "description": "角色描述",
            "personality": "性格特点"
        }}
    ],
    "dialogue": [
        {{
            "speaker": "说话者",
            "text": "对话内容",
            "translation": "中文翻译",
            "key_expressions": ["重点表达1", "重点表达2"],
            "cultural_notes": "文化注释"
        }}
    ],
    "key_vocabulary": ["重点词汇1", "重点词汇2"],
    "useful_phrases": ["实用短语1", "实用短语2"],
    "practice_tips": ["练习建议1", "练习建议2"],
    "extension_activities": ["扩展活动1", "扩展活动2"]
}}
"""

# 语法学习提示词
GRAMMAR_LEARNING_PROMPT = """
作为语法专家，请为用户制定语法学习计划：

用户水平：{current_level}
语法主题：{topic}
学习目标：{learning_goals}
常见错误：{common_errors}

请提供：
1. 语法点详细解释
2. 规则总结和例外情况
3. 大量例句展示
4. 常见错误和纠正方法
5. 练习题和应用
6. 学习进度安排

返回JSON格式：
{{
    "grammar_topic": "语法主题",
    "difficulty_level": "难度级别",
    "explanation": "详细解释",
    "rules": [
        {{
            "rule": "规则描述",
            "formula": "公式（如适用）",
            "examples": ["例句1", "例句2"],
            "exceptions": ["例外1", "例外2"]
        }}
    ],
    "common_errors": [
        {{
            "error": "错误示例",
            "correction": "正确形式",
            "explanation": "错误原因",
            "tip": "避免技巧"
        }}
    ],
    "practice_exercises": [
        {{
            "type": "题型",
            "question": "问题",
            "options": ["选项1", "选项2", "选项3", "选项4"],
            "answer": "正确答案",
            "explanation": "解释"
        }}
    ],
    "learning_tips": ["学习技巧1", "学习技巧2"]
}}
"""

# 进度评估提示词
PROGRESS_EVALUATION_PROMPT = """
作为学习评估专家，请评估用户的学习进度：

用户信息：
- 初始水平：{initial_level}
- 当前水平：{current_level}
- 学习时长：{study_duration} 周
- 完成活动：{completed_activities}
- 测试成绩：{test_scores}

请提供：
1. 进度详细分析
2. 能力提升评估
3. 学习效果量化
4. 优势和不足分析
5. 下阶段建议

返回JSON格式：
{{
    "overall_progress": "总体进度描述",
    "improvement_areas": {{
        "vocabulary": "词汇提升",
        "grammar": "语法提升",
        "listening": "听力提升",
        "speaking": "口语提升",
        "reading": "阅读提升",
        "writing": "写作提升"
    }},
    "achievements": ["成就1", "成就2"],
    "areas_for_improvement": ["需改进方面1", "需改进方面2"],
    "next_steps": ["下一步1", "下一步2"],
    "motivational_feedback": "激励反馈",
    "study_efficiency_score": 评分
}}
"""

# 所有提示词的集合
ENGLISH_LEARNING_PROMPTS = {
    "level_assessment": LEVEL_ASSESSMENT_PROMPT,
    "learning_plan": LEARNING_PLAN_PROMPT,
    "vocabulary_learning": VOCABULARY_LEARNING_PROMPT,
    "conversation_practice": CONVERSATION_PRACTICE_PROMPT,
    "grammar_learning": GRAMMAR_LEARNING_PROMPT,
    "progress_evaluation": PROGRESS_EVALUATION_PROMPT,
}
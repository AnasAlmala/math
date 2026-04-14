"""Seed the database with Arabic GRE Quant practice questions."""
import json


QUESTIONS = [
    # -----------------------------------------------------------------------
    # ARITHMETIC
    # -----------------------------------------------------------------------
    {
        "source": "Custom",
        "content_area": "Arithmetic",
        "question_type": "QC",
        "thinking_level": 1,
        "difficulty": 2,
        "trap_tags": ["fractions", "decimals"],
        "stem_ar": "قارن بين الكميتين:",
        "condition_ar": None,
        "col_a_ar": "3/7",
        "col_b_ar": "0.43",
        "choices": None,
        "correct_answer": "B",
        "solution_steps": [
            "حوّل الكسر إلى عشري: 3 ÷ 7 = 0.4286",
            "قارن: 0.4286 مقابل 0.43",
            "بما أن 0.43 > 0.4286 → العمود (ب) أكبر"
        ],
        "concept_explanation": "لمقارنة كسر بعشري حوّل الكسر إلى عشري أولاً",
        "decision_explanation": "دائماً اقسم الكسر لتحصل على القيمة الفعلية قبل المقارنة",
        "common_mistakes": ["ظنّ أن 3/7 أكبر لأن 7 > 4 — وهذا خطأ، قارن الأرقام بعد التحويل"],
    },
    {
        "source": "Custom",
        "content_area": "Arithmetic",
        "question_type": "MC",
        "thinking_level": 1,
        "difficulty": 1,
        "trap_tags": ["percentages"],
        "stem_ar": "كم يساوي 25% من 120؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": ["20", "25", "30", "40"],
        "correct_answer": "30",
        "solution_steps": [
            "25% = 1/4",
            "120 × (1/4) = 30"
        ],
        "concept_explanation": "النسبة المئوية تعني «من كل مئة»: 25% = 25/100 = 1/4",
        "decision_explanation": "حفظ المفاتيح: 25%=1/4، 50%=1/2، 75%=3/4 يوفّر الوقت",
        "common_mistakes": ["ضرب 120×25=3000 ونسيان القسمة على 100"],
    },
    {
        "source": "Custom",
        "content_area": "Arithmetic",
        "question_type": "NE",
        "thinking_level": 1,
        "difficulty": 1,
        "trap_tags": ["exponents"],
        "stem_ar": "ما ناتج 2⁵ ؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": None,
        "correct_answer": 32,
        "solution_steps": [
            "2¹ = 2",
            "2² = 4",
            "2³ = 8",
            "2⁴ = 16",
            "2⁵ = 32"
        ],
        "concept_explanation": "الأس يعني ضرب العدد في نفسه بعدد مرات الأس",
        "decision_explanation": "احفظ قوى 2 حتى 2¹⁰ — تظهر كثيراً في GRE",
        "common_mistakes": ["ضرب 2×5=10 بدلاً من 2×2×2×2×2=32"],
    },
    {
        "source": "Custom",
        "content_area": "Arithmetic",
        "question_type": "QC",
        "thinking_level": 3,
        "difficulty": 3,
        "trap_tags": ["sign", "variable"],
        "stem_ar": "قارن بين الكميتين:",
        "condition_ar": "n عدد صحيح موجب",
        "col_a_ar": "n² + n",
        "col_b_ar": "2n",
        "choices": None,
        "correct_answer": "D",
        "solution_steps": [
            "جرّب n=1: العمود أ = 1+1=2، العمود ب = 2 → متساويان",
            "جرّب n=2: العمود أ = 4+2=6، العمود ب = 4 → أ أكبر",
            "النتيجة تختلف بحسب قيمة n → لا يمكن التحديد (D)"
        ],
        "concept_explanation": "عندما تتغير العلاقة بتغيّر القيمة، الجواب دائماً D",
        "decision_explanation": "اختبر دائماً أكثر من قيمة واحدة. إذا اختلفت النتيجة → D",
        "common_mistakes": ["الافتراض أن n²+n > 2n دائماً دون اختبار n=1"],
    },
    # -----------------------------------------------------------------------
    # ALGEBRA
    # -----------------------------------------------------------------------
    {
        "source": "Custom",
        "content_area": "Algebra",
        "question_type": "MC",
        "thinking_level": 2,
        "difficulty": 2,
        "trap_tags": ["sign", "square_root"],
        "stem_ar": "إذا كان x² = 25، فما قيمة x ؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": ["5 فقط", "-5 فقط", "5 أو -5", "لا توجد إجابة"],
        "correct_answer": "5 أو -5",
        "solution_steps": [
            "x² = 25",
            "خذ الجذر التربيعي من الجانبين: |x| = 5",
            "إذن x = 5 أو x = -5"
        ],
        "concept_explanation": "المعادلة x²=k لها حلّان: x=√k و x=-√k (إذا k>0)",
        "decision_explanation": "كلّما رأيت x² تذكّر: هناك حلّان (موجب وسالب)",
        "common_mistakes": ["نسيان الحل السالب x=-5"],
    },
    {
        "source": "Custom",
        "content_area": "Algebra",
        "question_type": "NE",
        "thinking_level": 1,
        "difficulty": 1,
        "trap_tags": [],
        "stem_ar": "إذا كان 3x + 7 = 22، فما قيمة x ؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": None,
        "correct_answer": 5,
        "solution_steps": [
            "3x + 7 = 22",
            "3x = 22 - 7 = 15",
            "x = 15 ÷ 3 = 5"
        ],
        "concept_explanation": "لحل معادلة خطية: عزل المجهول بطرح وقسمة متتالية",
        "decision_explanation": "خطوات الحل: انقل الثابت، ثم اقسم على معامل x",
        "common_mistakes": ["طرح 7 خطأ: 22-7=15 صحيح، لكن بعضهم يحسبها 22+7=29"],
    },
    {
        "source": "Custom",
        "content_area": "Algebra",
        "question_type": "QC",
        "thinking_level": 2,
        "difficulty": 3,
        "trap_tags": ["sign", "variable", "fractions"],
        "stem_ar": "قارن بين الكميتين:",
        "condition_ar": "x ≠ 0",
        "col_a_ar": "x²",
        "col_b_ar": "x",
        "choices": None,
        "correct_answer": "D",
        "solution_steps": [
            "جرّب x=2: أ=4، ب=2 → أ أكبر",
            "جرّب x=0.5: أ=0.25، ب=0.5 → ب أكبر",
            "جرّب x=-1: أ=1، ب=-1 → أ أكبر",
            "النتيجة تتغير → D"
        ],
        "concept_explanation": "x² مقارنةً بـ x تعتمد على إشارة x وما إذا كان |x|<1 أو |x|>1",
        "decision_explanation": "اختبر: x>1، بين 0 و1، وسالب. إذا اختلفت النتائج → D",
        "common_mistakes": ["ظنّ أن x² أكبر دائماً لأن التربيع يُكبّر الأعداد — خاطئ للأعداد الكسرية"],
    },
    {
        "source": "Custom",
        "content_area": "Algebra",
        "question_type": "QC",
        "thinking_level": 2,
        "difficulty": 3,
        "trap_tags": ["sign", "variable"],
        "stem_ar": "قارن بين الكميتين:",
        "condition_ar": "x > 0",
        "col_a_ar": "x²",
        "col_b_ar": "x + 1",
        "choices": None,
        "correct_answer": "D",
        "solution_steps": [
            "جرّب x=0.5: أ=0.25، ب=1.5 → ب أكبر",
            "جرّب x=2: أ=4، ب=3 → أ أكبر",
            "النتيجة تتغير → D"
        ],
        "concept_explanation": "حتى مع الشرط x>0 يظل الجواب D لأن العلاقة تتغير",
        "decision_explanation": "لا تفترض أن الشرط يحسم الأمر — اختبر قيماً مختلفة",
        "common_mistakes": ["ظنّ أن x>0 تعني x² أكبر دائماً"],
    },
    {
        "source": "Custom",
        "content_area": "Algebra",
        "question_type": "MA",
        "thinking_level": 2,
        "difficulty": 3,
        "trap_tags": ["sign", "inequality"],
        "stem_ar": "أيّ من القيم التالية تحقّق المتراجحة x² < 4 ؟ (اختر كل ما ينطبق)",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": ["-3", "-1", "0", "1", "3"],
        "correct_answer": ["-1", "0", "1"],
        "solution_steps": [
            "x² < 4 تعني -2 < x < 2",
            "من الخيارات: -1 (✓)، 0 (✓)، 1 (✓)",
            "-3 و 3 خارج النطاق (-3²=9>4 و 3²=9>4)"
        ],
        "concept_explanation": "x² < k² يعادل -k < x < k (عندما k > 0)",
        "decision_explanation": "اكتب حل المتراجحة أولاً (-2<x<2) ثم تحقّق من كل خيار",
        "common_mistakes": ["نسيان الطرف السالب: -1 و 0 صحيحتان أيضاً"],
    },
    # -----------------------------------------------------------------------
    # GEOMETRY
    # -----------------------------------------------------------------------
    {
        "source": "Custom",
        "content_area": "Geometry",
        "question_type": "NE",
        "thinking_level": 1,
        "difficulty": 1,
        "trap_tags": [],
        "stem_ar": "ما مساحة مستطيل طوله 9 سم وعرضه 6 سم ؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": None,
        "correct_answer": 54,
        "solution_steps": [
            "مساحة المستطيل = الطول × العرض",
            "= 9 × 6 = 54 سم²"
        ],
        "concept_explanation": "مساحة المستطيل = ط × ع",
        "decision_explanation": "لا تخلط بين المساحة والمحيط: المحيط = 2(ط+ع)",
        "common_mistakes": ["حساب المحيط 2(9+6)=30 بدلاً من المساحة"],
    },
    {
        "source": "Custom",
        "content_area": "Geometry",
        "question_type": "MC",
        "thinking_level": 1,
        "difficulty": 1,
        "trap_tags": [],
        "stem_ar": "ما مجموع زوايا المثلث الداخلية؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": ["90°", "180°", "270°", "360°"],
        "correct_answer": "180°",
        "solution_steps": [
            "في أي مثلث: مجموع الزوايا الداخلية = 180°"
        ],
        "concept_explanation": "مجموع زوايا أي مثلث = 180° دائماً",
        "decision_explanation": "المربع = 360°، المثلث = 180°، لا تخلط بينهما",
        "common_mistakes": ["الخلط مع مجموع زوايا المربع (360°)"],
    },
    {
        "source": "Custom",
        "content_area": "Geometry",
        "question_type": "QC",
        "thinking_level": 2,
        "difficulty": 3,
        "trap_tags": ["pi", "comparison"],
        "stem_ar": "دائرة نصف قطرها r = 3:",
        "condition_ar": "r = 3",
        "col_a_ar": "محيط الدائرة (2πr)",
        "col_b_ar": "مساحة الدائرة (πr²)",
        "choices": None,
        "correct_answer": "B",
        "solution_steps": [
            "المحيط = 2π×3 = 6π ≈ 18.85",
            "المساحة = π×3² = 9π ≈ 28.27",
            "9π > 6π → العمود (ب) أكبر"
        ],
        "concept_explanation": "المحيط = 2πr، المساحة = πr². عند r=3: المساحة أكبر",
        "decision_explanation": "احسب العددين واقسم π للتبسيط: قارن 6 مع 9",
        "common_mistakes": ["الخلط بين صيغة المحيط والمساحة"],
    },
    # -----------------------------------------------------------------------
    # DATA ANALYSIS
    # -----------------------------------------------------------------------
    {
        "source": "Custom",
        "content_area": "DataAnalysis",
        "question_type": "NE",
        "thinking_level": 1,
        "difficulty": 1,
        "trap_tags": [],
        "stem_ar": "ما متوسط (mean) الأعداد: 4، 8، 12 ؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": None,
        "correct_answer": 8,
        "solution_steps": [
            "المجموع = 4 + 8 + 12 = 24",
            "العدد = 3",
            "المتوسط = 24 ÷ 3 = 8"
        ],
        "concept_explanation": "المتوسط الحسابي = مجموع الأعداد ÷ عددها",
        "decision_explanation": "إذا كانت الأعداد متساوية التباعد، المتوسط = الوسط (8 هو الوسط بين 4 و12)",
        "common_mistakes": ["قسمة المجموع على عدد خاطئ"],
    },
    {
        "source": "Custom",
        "content_area": "DataAnalysis",
        "question_type": "MC",
        "thinking_level": 1,
        "difficulty": 1,
        "trap_tags": ["median"],
        "stem_ar": "ما الوسيط (median) للمجموعة: {3، 5، 5، 7، 9} ؟",
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": ["3", "5", "6", "7"],
        "correct_answer": "5",
        "solution_steps": [
            "الأعداد مرتّبة: 3، 5، 5، 7، 9",
            "العدد الأوسط (الثالث من خمسة) = 5"
        ],
        "concept_explanation": "الوسيط هو العنصر الأوسط بعد الترتيب تصاعدياً",
        "decision_explanation": "رتّب الأعداد أولاً، ثم خذ العنصر الأوسط",
        "common_mistakes": ["أخذ المتوسط (5.8) بدلاً من الوسيط"],
    },
    {
        "source": "Custom",
        "content_area": "DataAnalysis",
        "question_type": "MC",
        "thinking_level": 2,
        "difficulty": 2,
        "trap_tags": ["average_update"],
        "stem_ar": (
            "كان متوسط درجات 4 طلاب 75. "
            "إذا انضمّ طالب خامس حصل على 100، "
            "فما متوسط الخمسة؟"
        ),
        "condition_ar": None,
        "col_a_ar": None,
        "col_b_ar": None,
        "choices": ["80", "85", "87.5", "90"],
        "correct_answer": "80",
        "solution_steps": [
            "مجموع الـ4 = 4 × 75 = 300",
            "المجموع الجديد = 300 + 100 = 400",
            "المتوسط الجديد = 400 ÷ 5 = 80"
        ],
        "concept_explanation": "عند إضافة عنصر: أوجد المجموع الكلي الجديد ثم اقسم على العدد الجديد",
        "decision_explanation": "لا تحسب متوسط المتوسطين (75+100)/2 — هذا خطأ شائع",
        "common_mistakes": ["حساب (75+100)/2 = 87.5 وهو خطأ"],
    },
]


def seed_if_empty():
    """Insert questions only if the table is empty."""
    from models import db, Question

    if Question.query.count() > 0:
        return

    for data in QUESTIONS:
        q = Question(
            source=data["source"],
            content_area=data["content_area"],
            question_type=data["question_type"],
            thinking_level=data["thinking_level"],
            difficulty=data["difficulty"],
            trap_tags_json=json.dumps(data["trap_tags"], ensure_ascii=False),
            stem_ar=data["stem_ar"],
            stem_en=None,
            condition_ar=data.get("condition_ar"),
            col_a_ar=data.get("col_a_ar"),
            col_b_ar=data.get("col_b_ar"),
            choices_json=(
                json.dumps(data["choices"], ensure_ascii=False)
                if data.get("choices")
                else None
            ),
            correct_answer_json=json.dumps(data["correct_answer"], ensure_ascii=False),
            solution_steps_json=json.dumps(
                data.get("solution_steps", []), ensure_ascii=False
            ),
            concept_explanation=data.get("concept_explanation"),
            decision_explanation=data.get("decision_explanation"),
            common_mistakes_json=json.dumps(
                data.get("common_mistakes", []), ensure_ascii=False
            ),
        )
        db.session.add(q)

    db.session.commit()
    print(f"[seed] Inserted {len(QUESTIONS)} questions.")

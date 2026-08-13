package com.example.ui

import androidx.compose.ui.Modifier
// تم إزالة دوال السحب (Swipe) لتعارضها مع التمرير العمودي الطبيعي
// يمكنك استخدام هذا الملف مستقبلاً لأي إيماءات مخصصة أخرى لا تتعارض مع الواجهة.

fun Modifier.emptyGestureModifier(): Modifier = this

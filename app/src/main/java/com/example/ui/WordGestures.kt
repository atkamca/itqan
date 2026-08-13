package com.example.ui

import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.PointerEventPass
import androidx.compose.ui.input.pointer.pointerInput

fun Modifier.swipeWatcher(
    onSwipeUp: () -> Unit,
    onSwipeDown: () -> Unit
): Modifier = this.pointerInput(Unit) {
    awaitPointerEventScope {
        while (true) {
            var event = awaitPointerEvent(PointerEventPass.Initial)
            var change = event.changes.firstOrNull()
            if (change == null || !change.pressed) continue
            
            val startY = change.position.y
            
            while (change != null && change.pressed) {
                event = awaitPointerEvent(PointerEventPass.Initial)
                change = event.changes.firstOrNull()
            }
            
            val endY = change?.position?.y ?: startY
            val deltaY = endY - startY
            
            if (deltaY > 40) {
                onSwipeDown() // User swiped down
            } else if (deltaY < -40) {
                onSwipeUp() // User swiped up
            }
        }
    }
}

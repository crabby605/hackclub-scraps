from machine import Pin, I2C, PWM
import ssd1306
import time

i2c = I2C(0, scl=Pin(28), sda=Pin(26))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

left_button = Pin(21, Pin.IN, Pin.PULL_UP)
right_button = Pin(17, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(2))

paddle_y = 24
ball_x = 64
ball_y = 32
ball_dx = 1
ball_dy = 1

while True:
    oled.fill(0)

    if not left_button.value():
        paddle_y -= 2
        if paddle_y < 0:
            paddle_y = 0
    if not right_button.value():
        paddle_y += 2
        if paddle_y > 48:
            paddle_y = 48

    oled.fill_rect(120, paddle_y, 8, 16, 1)

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_y <= 0 or ball_y >= 63:
        ball_dy = -ball_dy

    if ball_x >= 112 and paddle_y <= ball_y <= paddle_y + 16:
        ball_dx = -ball_dx
        buzzer.freq(1000)
        buzzer.duty_u16(500)
        time.sleep(0.1)
        buzzer.duty_u16(0)

    if ball_x <= 0 or ball_x >= 127:
        ball_x = 64
        ball_y = 32
        ball_dx = 1
        ball_dy = 1

    oled.fill_rect(ball_x, ball_y, 2, 2, 1)
    oled.show()
    time.sleep(0.05)


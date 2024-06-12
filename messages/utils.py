from PyQt5.QtCore import QEasingCurve


class MessageType(enumerate):
    Error = ("rgb(242, 222, 222)", "rgb(173, 106, 130)")
    Success = ("rgb(223, 240, 213)", "rgb(85, 135, 110)")
    Warning = ("rgb(252, 248, 225)", "rgb(159, 124, 54)")
    Alert = ("rgb(217, 237, 248)", "rgb(54, 113, 146)")


class EasingCurve(enumerate):
    Linear = QEasingCurve.Linear
    InQuad = QEasingCurve.InQuad
    OutQuad = QEasingCurve.OutQuad
    InOutQuad = QEasingCurve.InOutQuad
    OutInQuad = QEasingCurve.OutInQuad
    InCubic = QEasingCurve.InCubic
    OutCubic = QEasingCurve.OutCubic
    InOutCubic = QEasingCurve.InOutCubic
    OutInCubic = QEasingCurve.OutInCubic
    InQuart = QEasingCurve.InQuart
    OutQuart = QEasingCurve.OutQuart
    InOutQuart = QEasingCurve.InOutQuart
    OutInQuart = QEasingCurve.OutInQuart
    InQuint = QEasingCurve.InQuint
    OutQuint = QEasingCurve.OutQuint
    InOutQuint = QEasingCurve.InOutQuint
    OutInQuint = QEasingCurve.OutInQuint
    InSine = QEasingCurve.InSine
    OutSine = QEasingCurve.OutSine
    InOutSine = QEasingCurve.InOutSine
    OutInSine = QEasingCurve.OutInSine
    InExpo = QEasingCurve.InExpo
    OutExpo = QEasingCurve.OutExpo
    InOutExpo = QEasingCurve.InOutExpo
    OutInExpo = QEasingCurve.OutInExpo
    InCirc = QEasingCurve.InCirc
    OutCirc = QEasingCurve.OutCirc
    InOutCirc = QEasingCurve.InOutCirc
    OutInCirc = QEasingCurve.OutInCirc
    InElastic = QEasingCurve.InElastic
    OutElastic = QEasingCurve.OutElastic
    InOutElastic = QEasingCurve.InOutElastic
    OutInElastic = QEasingCurve.OutInElastic
    InBack = QEasingCurve.InBack
    OutBack = QEasingCurve.OutBack
    InOutBack = QEasingCurve.InOutBack
    OutInBack = QEasingCurve.OutInBack
    InBounce = QEasingCurve.InBounce
    OutBounce = QEasingCurve.OutBounce
    InOutBounce = QEasingCurve.InOutBounce
    OutInBounce = QEasingCurve.OutInBounce

F4:: {
    CoordMode("Mouse", "Screen")
    xpos := MouseGetPosX()
    ypos := MouseGetPosY()
    MsgBox("X" xpos " Y" ypos)
}

F12::Reload

MouseGetPosX() {
    MouseGetPos(&xpos, &ypos)
    return xpos
}

MouseGetPosY() {
    MouseGetPos(&xpos, &ypos)
    return ypos
}






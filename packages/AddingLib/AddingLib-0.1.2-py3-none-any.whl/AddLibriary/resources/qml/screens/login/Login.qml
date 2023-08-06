import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    anchors.fill: parent

    LoginForm {
        id: loginForm
    }

    Splash {
        id: splash
        anchors {
            left: loginForm.right
            right: parent.right
        }
    }

    Component.onCompleted: {
        __ga__.report("open", "login page")
    }
}
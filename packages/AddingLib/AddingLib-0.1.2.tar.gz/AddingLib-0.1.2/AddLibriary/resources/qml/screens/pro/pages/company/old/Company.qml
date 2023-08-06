import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: companyStack
    color: ui.colors.dark4

    property var createScreen: "qrc:/resources/qml/screens/pro/pages/company/Create.qml"
    property var waitScreen: "qrc:/resources/qml/screens/pro/pages/company/Wait.qml"

    Loader {
        id: companyLoader
        anchors.fill: parent
    }

    Component.onCompleted: {
        var temp = appUser.waiting_companies.length ? companyStack.waitScreen : companyStack.createScreen
        companyLoader.setSource(temp)
    }
}

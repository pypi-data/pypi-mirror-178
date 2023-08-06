import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
//  Icon alias
    property alias companyImage: companyImage
//  Main text
    property alias atomTitle: atomTitle

    implicitWidth: parent.width
    height: Math.max(atomTitle.height + 24, 64)

    color: ui.ds3.bg.highest

    DS3.CompanyImage {
        id: companyImage

        anchors {
            left: parent.left
            leftMargin: 16
            top: parent.top
            topMargin: 12
        }

        name: atomTitle.title
        opacity: enabled ? 1 : 0.3
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: companyImage.right
            leftMargin: 16
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        opacity: enabled ? 1 : 0.3
    }
}
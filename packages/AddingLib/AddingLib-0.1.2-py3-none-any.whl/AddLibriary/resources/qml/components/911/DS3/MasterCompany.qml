import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: masterCompany

//  Image of the company
    property alias companyImage: companyImage
//  Company name
    property alias companyName: companyName

    implicitWidth: parent.width
    implicitHeight: 68

    color: ui.ds3.figure.transparent

    DS3.CompanyImage {
        id: companyImage

        anchors {
            left: parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }

        name: companyName.text
    }

    Rectangle {
        id: circle

        anchors.fill: companyImage

        radius: width / 2
        visible: false
    }

    DS3.Text {
        id: companyName

        anchors {
            verticalCenter: parent.verticalCenter
            left: companyImage.right
            leftMargin: 16
            right: parent.right
            rightMargin: 24
        }

        hasElide: true
        style: ui.ds3.text.body.LBold
    }
}

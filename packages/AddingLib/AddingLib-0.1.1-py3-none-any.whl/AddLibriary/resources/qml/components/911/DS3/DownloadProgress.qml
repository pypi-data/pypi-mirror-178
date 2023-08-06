import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Item {
    id: downloadProgress

//  Use for changing title and subtitle
    property alias atomTitle: atomTitle
//  Use for changing spinner item
    property alias spinnerItem: spinnerItem
//
    property bool isSpinner: true

    signal cancelButtonClicked()

    width: 268
    height: 48

    DS3.Icon {
        id: pdfIcon

        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/maintenance_report/Icon_PDF.svg"
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: pdfIcon.right
            leftMargin: 8
            right: spinnerItem.left
            rightMargin: 8
        }

        titleItem.hasElide: true
    }

    DS3.Spinner {
        id: spinnerItem

        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }

        size: DS3.Spinner.ImageSize.M
        visible: isSpinner
    }

    DS3.Image {
        id: cancelButton

        anchors.fill: spinnerItem

        source: "qrc:/resources/images/Athena/common_icons/AtomStatusClose-M.svg"
        visible: !isSpinner

        DS3.MouseArea {
            onEntered: isSpinner = false
            onExited: isSpinner = true
            onClicked: onCancelButtonClicked()
        }
    }

    DS3.MouseArea {
        anchors.fill: spinnerItem

        onEntered: isSpinner = false
        onExited: isSpinner = true
        onClicked: cancelButtonClicked()
    }
}
import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
//  List of titles and descriptions
    property var sections

    width: 500

    DS3.Spacing {
        height: 24
    }

    DS3.Icon {
        anchors.horizontalCenter: parent.horizontalCenter

        source: "qrc:/resources/images/Athena/common_icons/InfoFilled-M.svg"
    }

    DS3.Spacing {
        height: 24
    }

    Repeater {
        id: repeater

        model: sections

        Column {
            width: parent.width

            DS3.Text {
                id: titleText

                width: parent.width

                style: ui.ds3.text.title.MBold
                text: !!modelData.title ? modelData.title : ""
                horizontalAlignment: Text.AlignHCenter
                visible: !!modelData.title
            }

            DS3.Spacing {
                height: 8
            }

            DS3.Text {
                id: descriptionText

                width: parent.width

                style: ui.ds3.text.body.LRegular
                text: !!modelData.description ? modelData.description : ""
                horizontalAlignment: Text.AlignHCenter
                color: ui.ds3.figure.secondary
                visible: !!modelData.description
            }

            DS3.Spacing {
                height: 24
            }
        }
    }
}

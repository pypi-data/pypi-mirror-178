import QtQuick 2.7

Item {
    id: wizardWarning

    width: row.width
    height: row.height

    Row {
        id: row

        height: warningImage.height > warningText.height ? warningImage.height : warningText.height
        spacing: 8

        Image {
            id: warningImage

            width: 16
            height: 16

            sourceSize.width: 16
            sourceSize.height: 16

            source: "qrc:/resources/images/icons/ic-warning-info.svg"

            anchors.verticalCenter: warningText.verticalCenter
        }

        Text {
            id: warningText

            text: tr.settings_are_not_PD6662_compliant

            font.family: roboto.name
            font.pixelSize: 11
            font.weight: Font.Light
            color: "#ea3323"
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter

        }
    }
}
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.TitleLeftAlign {
//  When clicked on button
    property var onButtonClicked: () => {}
//  Button text (use with hasButton)
    property alias buttonText: textButton.text
//  Transparent bg
    property bool isBgTransparent: false

    color: isBgTransparent ? ui.ds3.figure.transparent : ui.ds3.bg.high

    textItem {
        anchors {
            leftMargin: 16
            right: textButton.left
            rightMargin: 16
        }
    }

    DS3.ButtonSelect {
        id: textButton

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        textButtonMouseArea.onClicked: onButtonClicked()
    }
}

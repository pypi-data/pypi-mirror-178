import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    height: parent.height
    clip: true

    function get_current_time() {
        var today = new Date();
        /*if (today.getFullYear() < 1970) {
            today.setFullYear(today.getFullYear() + 100)
            console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", today)
        }*/
        var time = today.toLocaleTimeString(
            application.locale,
            settings.is_ampm_time_format ? "hh:mm:ss ap": "HH:mm:ss")
        var date = today.toLocaleDateString(application.locale, Locale.LongFormat)
        return [time, date]
    }

    /*RadialGradient {
        anchors.fill: parent
        visible: false
        verticalOffset: -parent.height / 2
        horizontalOffset: -parent.width / 2
        gradient: Gradient{
            GradientStop { position: 0.0; color: "#272b32" }
            GradientStop { position: 1.0; color: "#1d1f23" }
        }
    }*/

    Image {
        id: backgroundImage
        width: parent.width
        source: "qrc:/resources/images/temporary/background.png"
        sourceSize.width: width
        sourceSize.height: height

        clip: true
        fillMode: Image.PreserveAspectCrop
        verticalAlignment: Image.AlignVCenter
        horizontalAlignment: Image.AlignRight

        anchors {
            top: parent.top
            right: parent.right
            bottom: parent.bottom
        }

        /* ------------------------------------------------ */
        /* desktop tests */
        Accessible.name: "login_background_image"
        Accessible.description: source
        Accessible.role: Accessible.Graphic
        /* ------------------------------------------------ */
    }

    Item {
        id: dateTime
        width: 200
        height: 80
        anchors {
            right: parent.right
            bottom: parent.bottom
            rightMargin: 80
            bottomMargin: 46
        }

        Component.onCompleted: {
            Number.prototype.pad = function(len) {
                return (new Array(len+1).join("0") + this).slice(-len);
            }
        }

        Timer {
            id: dateTimer
            interval: 1000
            repeat: true
            running: false
            triggeredOnStart: true

            onTriggered: {
                var time = get_current_time()
                dateTimeText.text = time[0]
                dateText.text = time[1]
            }
        }

        Custom.FontText {
            id: dateTimeText
            font.pixelSize: 36
            color: ui.colors.white
            horizontalAlignment: Text.AlignRight
            anchors {
                right: parent.right
                top: parent.top
            }

            Component.onCompleted: {
                dateTimer.start()
            }
        }

        Custom.FontText {
            id: dateText
            font.pixelSize: 24
            color: ui.colors.white
            font.capitalization: Font.Capitalize
            horizontalAlignment: Text.AlignRight
            anchors {
                right: parent.right
                bottom: parent.bottom
            }
        }
    }
}
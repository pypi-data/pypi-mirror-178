import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Popup {

    width: 400

    DS3.Icon {
        anchors.horizontalCenter: parent.horizontalCenter

        source: "qrc:/resources/images/Athena/common_icons/InfoFilled-M.svg"
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        width: parent.width

        text: tr.disabled_power_insufficient_description
        style: ui.ds3.text.body.MRegular
        horizontalAlignment: Text.AlignHCenter
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        width: parent.width

        text: {
            var language = tr.get_locale() || "en"
            if (language == "ru_UA") { language = "uk" }
            if (language == "cs") { language = "cz" }
            var device_type = "44"
            var link = "http://instructionservice.ops.ajax.systems/manual/" + device_type + "?lang="+ language
            return util.hyperlink(tr.disabled_power_insufficient_link, link)
        }
        style: ui.ds3.text.body.MRegular
        horizontalAlignment: Text.AlignHCenter
        color: ui.ds3.figure.interactive
    }

    DS3.Spacing {
        height: 24
    }
}

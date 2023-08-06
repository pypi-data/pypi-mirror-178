import QtQuick 2.14
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Column {
//  Enum with Footer types
    enum FooterType {
        Device,     // default
        User
    }
//  Type of the footer
    property var footerType: DS3.InfoFooter.FooterType.Device
//  Property when need to change title text
    property alias title: title
//  Property when need to change iD text
    property alias subtitleUpper: subtitleUpper
//  Property when need to change deviceNumber text
    property alias subtitleLower: subtitleLower

    width: parent.width
    height: footerType == DS3.InfoFooter.FooterType.Device ? 85 : 64

    DS3.Spacing {
        height: footerType == DS3.InfoFooter.FooterType.Device ? 12 : 16
    }

    DS3.Text {
        id: title

        width: parent.width
        height: !!text ? undefined : 0

        horizontalAlignment: Text.AlignHCenter
        textFormat: Text.RichText
    }

    DS3.Text {
        id: subtitleUpper

        width: parent.width
        height: !!text ? undefined : 0

        horizontalAlignment: Text.AlignHCenter
        textFormat: Text.RichText
        color: ui.ds3.figure.secondary
    }

    DS3.Text {
        id: subtitleLower

        width: parent.width
        height: !!text ? undefined : 0

        horizontalAlignment: Text.AlignHCenter
        textFormat: Text.RichText
        color: ui.ds3.figure.secondary
    }
}
import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3

DS3.UserNavigation {
    image: !!user.small_image_link && user.small_image_link != "WRONG" ? user.small_image_link : ""
    atomTitle {
        title: user.name
        subtitle: user.email
    }
    role: {
        if (!user || !user.hub_role) return ""
        if (user.hub_role == "USER") return tr.user
        if (user.hub_role == "MASTER") return tr.admin
        if (user.hub_role == "PRO") return tr.pro
        return ""
    }
    hasPrivacyOfficerBadge: user.privacy_access_settings == true && hub.show_privacy_officer_badge && user.hub_role != "PRO"

    onRightIconClicked: {
        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UserSettings.qml", {"user": user})
    }
}
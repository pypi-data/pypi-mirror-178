import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.user
        subtitle: {
            let user_id = device.associated_user_id;
            if (user_id == "00000000") return tr.guest_user
            let user = management.users.get_user(user_id)
            return user.name ? user.name : tr.user_was_deleted
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/User-M.svg"
}

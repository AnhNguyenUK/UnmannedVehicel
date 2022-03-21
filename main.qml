import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Layouts 1.12
import QtLocation 5.6
import QtPositioning 5.6

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    property real coorlat: 0.0
    property real coorLong: 0.0

    Plugin {
    id: mapPlugin
    name: "osm" // "mapboxgl", "esri", ...
    // specify plugin parameters if necessary
    // PluginParameter {
    //     name:
    //     value:
    // }
    }

    RowLayout{
        anchors.fill:parent
        spacing: 6
        Map {
            id: mapSection
            Layout.fillWidth: true
            Layout.minimumWidth: 100
            Layout.preferredWidth: 100
            Layout.maximumWidth: parent.width - infoList.width - parent.spacing
            Layout.minimumHeight: parent.height
            plugin: mapPlugin
            center: QtPositioning.coordinate(59.91, 10.75) // Oslo
            zoomLevel: 100
            Component.onCompleted:{
                map.addMapItem(mapItem)
            }

            MapQuickItem {
                id: mapItem
                coordinate: QtPositioning.coordinate(59.91, 10.75)

                anchorPoint.x: image.width
                anchorPoint.y: image.height

                sourceItem: Column {
                    Image {
                        id: image
                        source: "marker.png"
                        width: 20
                        height: 20
                    }

                    // Rectangle{
                    //     id: marker
                    //     width: 100
                    //     height: 100
                    //     radius: 50
                    //     color: "red"
                    // }
                }
            }
        }
        ListView{
            id: infoList
            Layout.fillWidth: true
            Layout.minimumWidth: 100
            Layout.preferredWidth: 100
            Layout.maximumWidth: 150
            Layout.minimumHeight: parent.height
            clip: true
            model: dataModel.model
            spacing: 5
            delegate: Component{
                GPSItem{
                    currLat: modelCurrLat
                    currLon: modelCurrLong
                    robotId: modelRobotId
                    Layout.fillWidth: true
                    width: parent.width
                    height: 70
                }
            }
            ListModel{
                id: testModel
                ListElement{
                    modelCurrLat: "15"
                    modelCurrLong: "20"
                    modelRobotId: "Robot1"
                }
                ListElement{
                    modelCurrLat: "15"
                    modelCurrLong: "20"
                    modelRobotId: "Robot1"
                }
                ListElement{
                    modelCurrLat: "15"
                    modelCurrLong: "20"
                    modelRobotId: "Robot1"
                }
            }

        }
        function getCoordinate(n_Lat,n_Long){
            coorlat = n_Lat
            coorLong = n_Long
            console.log("Latitude: ",n_Lat," ,Longtitude: ",n_Long);
        }
    }
}

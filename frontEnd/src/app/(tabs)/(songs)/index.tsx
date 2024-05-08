import { defaultStyles } from "@/styles"
import { ScrollView, Text, View } from "react-native"
import { TrackList } from "@/components/TrackList"
import { screenPadding } from "@/constants/tokens"
import { useNavigationSearch } from "@/hooks/useNavigationSearch"
import library from '@/assets/data/library.json'
import { useMemo } from "react"
import { trackTitleFilter } from "@/helpers/filter"
import { useTracks } from "@/store/library"
import { generateTracksListId } from "@/helpers/miscellaneous"
import { Link } from "expo-router"

const SongsScreen = () => {

    const search = useNavigationSearch({
        searchBarOptions: {
            placeholder: 'Find in Songs'
        }
    })

    const tracks = useTracks()

    const filteredTracks = useMemo(() => {
        if(!search) return tracks

        return library.filter(trackTitleFilter(search))
    }, [search, tracks])

    return (
        <View style={defaultStyles.container}>
            <ScrollView contentInsetAdjustmentBehavior="automatic"
                        style={{ paddingHorizontal: screenPadding.horizontal}}>
                <TrackList id={generateTracksListId('songs', search)} tracks={filteredTracks} scrollEnabled={false}/>
            </ScrollView>
        </View>
    )
}

export default SongsScreen
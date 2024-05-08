import { defaultStyles } from "@/styles"
import { View } from "react-native"
import { Stack } from "expo-router"
import { StackScreenWithSearchBar } from "@/constants/layout"

const registrationScreenLayout = () => {
return (
    <View style={defaultStyles.container}>
        <Stack>
            <Stack.Screen
            name="index"
            options={{
                ...StackScreenWithSearchBar,
                headerTitle: 'Registration',
            }}
            />
        </Stack>
    </View>

)}

export default registrationScreenLayout
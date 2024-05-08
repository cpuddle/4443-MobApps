import { colors } from '@/constants/tokens'
import { useLogTrackPlayerState } from '@/hooks/useLogTrackPlayerState'
import { useSetupTrackPlayer } from '@/hooks/useSetupTrackPlayer'
import { SplashScreen, Stack } from 'expo-router'
import { StatusBar } from 'expo-status-bar'
import { useCallback } from 'react'
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import { SafeAreaProvider } from 'react-native-safe-area-context'
import TrackPlayer from 'react-native-track-player'
import "global.css"



const App = () => {
	const handleTrackPlayerLoaded = useCallback(() => {
		SplashScreen.hideAsync()
	}, [])

	useSetupTrackPlayer({
		onLoad: handleTrackPlayerLoaded,
	})

	useLogTrackPlayerState()

    return (
      <SafeAreaProvider>
          <GestureHandlerRootView style={{flex:1}}>
            <RootNavigation />
            <StatusBar style='auto' />
          </GestureHandlerRootView>
      </SafeAreaProvider>
    )
}

const RootNavigation = () => {
    return (
      <Stack initialRouteName='(login)'>
        <Stack.Screen name='(tabs)' options={{headerShown:false}}/>
        <Stack.Screen name='(login)' options={{headerShown: false}}/>
        <Stack.Screen name='(registration)' options={{headerShown: false}}/>
        <Stack.Screen name='player' options={{
          presentation: 'card',
          gestureEnabled: true,
          gestureDirection: 'vertical',
          animationDuration: 400,
          headerShown: false,
        }}/>
      </Stack>
    )
}

export default App
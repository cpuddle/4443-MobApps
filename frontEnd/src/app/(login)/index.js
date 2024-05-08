import React, { useState } from 'react';
import { View, TextInput, Button, Text, Alert, TouchableOpacity } from 'react-native';
import { defaultStyles } from "@/styles"
import { Link } from 'expo-router';


const LoginScreen = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // Implement login logic here
    // Example POST request to your FastAPI backend
    fetch('...', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.success) {
        // Navigate to the home page
        // navigation.navigate('Home');// Replace 'HomePage' with the actual name of your home page route
        return (
          <Link replace href={"(tabs)/(songs)"}>
          </Link>
        )
      } else {
        // Handle unsuccessful login
        Alert.alert('Login Failed', 'Invalid email or password');
      }

      // Handle navigation or state update here based on response
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <View style={defaultStyles.container} className='flex-1 justify-center items-center'>
      <TextInput 
        className='text-white text-2xl'
        onChangeText={setEmail}
        value={email}
        placeholder="Email"
        autoCapitalize='none'
        keyboardType="email-address"
      />
      <TextInput
        className="text-white text-2xl"
        onChangeText={setPassword}
        value={password}
        placeholder="Password"
        autoCapitalize='none'
        secureTextEntry
      />
      
      <View>
        <View className="p-2 m-3 bg-yellow font-bold  border border-yellow rounded-full">
            <Link replace href={"(tabs)/(songs)"}><Text>   Login</Text></Link>
        </View>
        <View className='items-center'>
          <Text className='text-white'>Register Here</Text>
          <View className='p-2 m-3 px-3 bg-yellow font-bold  border border-yellow rounded-full'><Link replace href={"(registration)"}><Text>Register</Text></Link></View>
        </View>
      </View>
    </View>
  );
};


export default LoginScreen
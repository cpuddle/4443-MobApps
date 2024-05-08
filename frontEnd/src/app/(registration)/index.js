import { Link } from 'expo-router';
import React, { useState } from 'react';
import { View, TextInput, Button, Text, TouchableOpacity, StyleSheet } from 'react-native';

const RegistrationScreen = () => {
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = () => {
    // Implement registration logic here
    // Example POST request to your FastAPI backend
    fetch('...', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        first_name: first_name,
        last_name: last_name,
        username: username,
        email: email,
        password: password,
      }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      return (
        <Link replace href="(login)"></Link>
      )
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
      <View style={styles.container} className={"flex-1 justify-center items-center"}>
      <TextInput
        // style={tailwind('border border-gray-300 p-2 rounded mb-4')}
        className="text-2xl text-white"
        onChangeText={setFirstName}
        value={first_name}
        placeholder="First Name"
        autoComplete='none'
        autoCapitalize='none'
      />
      <TextInput
        // style={tailwind('border border-gray-300 p-2 rounded mb-4')}
        className="text-2xl text-white"
        onChangeText={setLastName}
        value={last_name}
        placeholder="Last Name"
        autoComplete='none'
        autoCapitalize='none'
      />
      <TextInput
        // style={tailwind('border border-gray-300 p-2 rounded mb-4')}
        className="text-2xl text-white"
        onChangeText={setUsername}
        value={username}
        autoCapitalize='none'
        placeholder="Username"
        autoComplete='none'
      />
      <TextInput
        // style={tailwind('border border-gray-300 p-2 rounded mb-4')}
        className="text-2xl text-white"
        onChangeText={setEmail}
        value={email}
        placeholder="Email"
        autoCapitalize='none'
        keyboardType="email-address"
        autoComplete='none'
      />
      <TextInput
        // style={tailwind('border border-gray-300 p-2 rounded mb-4')}
        className="text-2xl text-white"
        onChangeText={setPassword}
        value={password}
        placeholder="Password"
        autoCapitalize='none'
        secureTextEntry
        autoComplete='none'
      />

      <View className="p-2 m-3 px-3 bg-yellow font-bold  border border-yellow rounded-full">
        <TouchableOpacity onPress={handleRegister}><Text>Register</Text></TouchableOpacity>  
      </View>
      <View className="justify-center items-center">
        <Text className={"text-white"}>Already registered?</Text>
        <View className="p-2 m-3 px-3 bg-yellow font-bold  border border-yellow rounded-full">
          <Link replace href={"(login)"}><Text className={"text-black"}>Login Here</Text></Link>
        </View>
        
      </View>
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#282828',
    alignContent: 'center',
    justifyContent: 'center',
    color: '#ebdbb2'
  }
})
export default RegistrationScreen;
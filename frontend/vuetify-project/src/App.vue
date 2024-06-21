<template>
  <v-app>
    <h1 class="text-center text-6xl font-bold text-purple-700 py-5">
      image app
    </h1>

    <div class="flex flex-col items-center space-y-4 mt-5">
      <v-chip
        v-if="newImages > 0"
        class="text-black border-2 border-purple-500 rounded-lg px-4 py-2"
      >{{ newImages }} new images</v-chip>
      <v-btn
        @click="downloadImages"
        class="bg-purple-500 text-black rounded-lg px-4 py-2 hover:bg-purple-700"
      >Download Images</v-btn>
    </div>
    <div
      v-if="images.length > 0"
      class="max-h-screen d-flex justify-center items-center bg-purple-100"
    >
      <ImageGallery :images="images" :pageSize="4" />
    </div>
  </v-app>
</template>

<script lang="js">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'
import { createVuetify } from 'vuetify'
import ImageGallery from "./components/ImageGallery.vue"

import axios from 'axios'

export default defineComponent({
  name: 'App',
  components: {
    ImageGallery
  },
  setup() {
    const vuetify = createVuetify()
    const inputValue = ref(0)
    const isError = ref(false)
    const newImages = ref(0)
    const images = ref([])
    let socket = null

    const downloadImages = async () => {
      newImages.value = 0

      try {
        const response = await axios.get('http://localhost:8000/images/')
        images.value = response.data
      } catch (error) {
        console.error(error)
      }
    }

    const connectWebSocket = () => {
      socket = new WebSocket('ws://localhost:8000/ws')

      socket.onopen = () => {
        console.log('WebSocket is connected.')
        newImages.value = 0
      }

      socket.onmessage = event => {
        console.log(`WebSocket message: ${event.data}`)
        try {
          const data = JSON.parse(event.data)
          newImages.value += data.number_of_images
          console.log(`New images: ${newImages.value}`)
        } catch (error) {
          console.error(`Error parsing WebSocket message: ${error}`)
        }
      }

      socket.onerror = error => {
        console.error(`WebSocket error: ${error}`)
      }

      socket.onclose = event => {
        console.log(
          'WebSocket is closed.',
          event.reason
        )
        setTimeout(connectWebSocket, 1000)
      }
    }

    onMounted(connectWebSocket)

    onUnmounted(() => {
      if (socket) {
        socket.close()
      }
    })

    return {
      vuetify,
      inputValue,
      isError,
      newImages,
      images,
      downloadImages
    }
  }
})

</script>


<script>
  import { querystring } from 'svelte-spa-router'
  import qs from 'qs'

  $: query = qs.parse($querystring)
  $: name = query.name || '팀 : Findrama'
  $: email = query.email || '변효근'
  $: blog = query.blog || '이준규'
  $: phone = query.phone || '이정은'
  
</script>

<div class="user-profile">
  <div class="photos">
    <div class="photo">
      <img src="/assets/mango.jpg" alt="User">
    </div>
    <div class="photo">
      <img src="/assets/mango.jpg" alt="User">
    </div>
    <div class="photo">
      <img src="/assets/mango.jpg" alt="User">
    </div>
  </div>
  <div class="details">
    <div class="name">{name}</div>
    <div class="email">{email}</div>
    <div class="blog">{blog}</div>
    <div class="phone">{phone}</div>
  </div>
</div>

<style lang="scss">
  .user-profile {
    padding: 80px 0;
    .photos {
      display: flex;
      justify-content: center;
      .photo {
        flex-shrink: 0;
        width: 230px;
        height: 230px;
        padding: 30px;
        box-sizing: border-box;
        background-color: $color--area;
        border-radius: 50%;
        border: 12px solid $color--black;
        
        img {
          width: 100%;
        }
      }
    }
    .details {
      margin-top: 20px;
      text-align: center;
      .name {
        font-size: 40px;
        font-family: 'Oswald', sans-serif;
        margin-bottom: 20px;
      }
    }
  }
</style>

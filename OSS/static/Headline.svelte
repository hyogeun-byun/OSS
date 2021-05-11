<div class="headline">
  <h1>
    <span>Findrama</span><br />
    드라마 검색<br />
    드라마 평가
  </h1>
  <div class="description">
    <p>
      드라마 검색을 위한 Search페이지와 드라마 평가를 위한 Drama페이지로 이루어져있다.
    </p>
    <p>
      드라마는 장르, 방영연도, 이름으로 검색이 가능하다.
    </p>
  </div>
</div>

<style lang="scss">
  .headline {
    h1 {
      line-height: 1;
      font-family: 'Oswald', sans-serif;
      font-size: 80px;
      @media #{$mobile} {
        font-size: 60px;
      }
      span {
        color: $color--primary;
      }
    }
    .description {
      margin: 30px 0;
      color: $color--white-30;
    }
  }
</style>

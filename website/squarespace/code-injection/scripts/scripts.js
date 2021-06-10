const getCookie = (cookieField) => document.cookie.split('; ').reduce((result, cookie) => {
    if (
      cookie.split('=')[0] === cookieField
              && cookie.split('=')[1] !== 'null'
    ) {
      return cookie.split('=')[1];
    }
  
    return result;
  }, '');
  
  const setCookie = (cookieField, cookieValue, expires) => {
    document.cookie = `${cookieField}=${cookieValue}; path=/; expires=${expires.toUTCString()}`;
  };
  
  const deleteCookie = (cookieField) => {
    document.cookie = `${cookieField}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
  };
  
  const getAccessTokenFromCookies = () => {
    const token = getCookie('token');
    const tokenType = getCookie('tokenType');
    if (!token) {
      return ['', ''];
    }
  
    return [token, tokenType];
  };
  
  const getAccessTokenFromFragment = () => {
    const fragment = new URLSearchParams(window.location.hash.slice(1));
    const [token, tokenType] = [
      fragment.get('access_token'),
      fragment.get('token_type'),
    ];
    if (!token) {
      return ['', ''];
    }
    const msPerMinute = 60000;
    const tenMinutesFromNow = new Date(new Date().getTime() + 10 * msPerMinute);
    setCookie('token', token, tenMinutesFromNow);
    setCookie('tokenType', tokenType, tenMinutesFromNow);
  
    return [token, tokenType];
  };
  
  const getAccessToken = () => {
    let [token, tokenType] = getAccessTokenFromCookies();
    if (token !== '') {
      return [token, tokenType];
    }
    [token, tokenType] = getAccessTokenFromFragment();
  
    return [token, tokenType];
  };
  
  const getHeaderNavList = () => document.getElementsByClassName('header-nav-list')[0];
  
  const createUserNavItemFolderTitle = (response) => {
    const {
      id, avatar,
    } = response;
    const userNavItemFolderTitle = document.createElement('a');
    userNavItemFolderTitle.setAttribute('id', 'user-nav-item-folder-title');
    userNavItemFolderTitle.innerHTML = `<img class='avatar' src='https://cdn.discordapp.com/avatars/${id}/${avatar}.png'>`;
  
    return userNavItemFolderTitle;
  };
  
  const createUserNavItemFolderContentUserInfo = (response) => {
    const {
      id, username, discriminator, avatar,
    } = response;
    const userNavItemFolderContentUserInfo = document.createElement('div');
    userNavItemFolderContentUserInfo.classList.add(
      'header-nav-folder-item',
      'header-nav-folder-item--external',
    );
    userNavItemFolderContentUserInfo.setAttribute('id', 'user-nav-item-folder-content');
    userNavItemFolderContentUserInfo.innerHTML = `<img class='avatar' src='https://cdn.discordapp.com/avatars/${id}/${avatar}.png'><div class='user-menu-text'>${username}#${discriminator}</div>`;
  
    return userNavItemFolderContentUserInfo;
  };
  
  const createUserNavItemFolderContentServersAnchor = () => {
    const userNavItemFolderContentServersAnchor = document.createElement('a');
    userNavItemFolderContentServersAnchor.setAttribute('href', '/servers');
    userNavItemFolderContentServersAnchor.innerText = 'Servers';
  
    return userNavItemFolderContentServersAnchor;
  };
  
  const createUserNavItemFolderContentServers = () => {
    const userNavItemFolderContentServers = document.createElement('div');
    userNavItemFolderContentServers.classList.add(
      'header-nav-folder-item',
      'header-nav-folder-item--external',
    );
    userNavItemFolderContentServers.appendChild(
      createUserNavItemFolderContentServersAnchor(),
    );
  
    return userNavItemFolderContentServers;
  };
  
  const clearCookies = () => {
    deleteCookie('token');
    deleteCookie('tokenType');
  };
  
  const redirectToHome = () => { window.location.href = '/'; };
  
  const performLogOut = () => {
    clearCookies();
    redirectToHome();
  };
  
  const createUserNavItemFolderContentLogOutAnchor = () => {
    const userNavItemFolderContentLogOutAnchor = document.createElement('a');
    userNavItemFolderContentLogOutAnchor.setAttribute('href', '#');
    userNavItemFolderContentLogOutAnchor.onclick = performLogOut;
    userNavItemFolderContentLogOutAnchor.innerText = 'Log out';
  
    return userNavItemFolderContentLogOutAnchor;
  };
  
  const createUserNavItemFolderContentLogOut = () => {
    const userNavItemFolderContentLogOut = document.createElement('div');
    userNavItemFolderContentLogOut.classList.add(
      'header-nav-folder-item',
      'header-nav-folder-item--external',
    );
    userNavItemFolderContentLogOut.appendChild(
      createUserNavItemFolderContentLogOutAnchor(),
    );
  
    return userNavItemFolderContentLogOut;
  };
  
  const createUserNavItemFolderContent = (response) => {
    const userNavItemFolderContent = document.createElement('div');
    userNavItemFolderContent.classList.add('header-nav-folder-content');
    userNavItemFolderContent.appendChild(createUserNavItemFolderContentUserInfo(response));
    userNavItemFolderContent.appendChild(createUserNavItemFolderContentServers());
    userNavItemFolderContent.appendChild(createUserNavItemFolderContentLogOut());
  
    return userNavItemFolderContent;
  };
  
  const createUserNavItem = (response) => {
    const userNavItem = document.createElement('div');
    userNavItem.classList.add('header-nav-item', 'header-nav-item--folder');
    userNavItem.appendChild(createUserNavItemFolderTitle(response));
    userNavItem.appendChild(createUserNavItemFolderContent(response));
  
    return userNavItem;
  };
  
  const addUserMenuForDesktop = (response) => {
    getHeaderNavList().appendChild(createUserNavItem(response));
  };
  
  const removeLogInButtonForDesktop = () => document
    .getElementsByClassName('btn btn--border theme-btn--primary-inverse')[0]
    .remove();
  
  const getHeaderMobileMenu = () => document
    .getElementsByClassName('header-menu-nav-folder-content')[0];
  
  const createServersMenuItemAnchor = () => {
    const serversMenuItemAnchor = document.createElement('a');
    serversMenuItemAnchor.setAttribute('href', '/servers');
    serversMenuItemAnchor.innerText = 'Servers';
  
    return serversMenuItemAnchor;
  };
  
  const createServersMenuItem = () => {
    const serversMenuItem = document.createElement('div');
    serversMenuItem.classList.add(
      'container',
      'header-menu-nav-item',
      'header-menu-nav-item--collection',
    );
    serversMenuItem.appendChild(createServersMenuItemAnchor());
  
    return serversMenuItem;
  };
  
  const addServersMenuItemForMobile = () => {
    getHeaderMobileMenu().appendChild(createServersMenuItem());
  };
  
  const replaceLogInWithLogOutForMobile = () => {
    const mobileMenuCta = document.getElementsByClassName('header-menu-cta')[0];
    const logOut = mobileMenuCta.children[0];
    logOut.setAttribute('href', '#');
    logOut.innerText = 'Log out';
    logOut.onclick = performLogOut;
  };
  
  window.onload = () => {
    const [token, tokenType] = getAccessToken();
    if (!token) {
      return;
    }
  
    fetch('https://discord.com/api/users/@me', {
      headers: {
        authorization: `${tokenType} ${token}`,
      },
    })
      .then((result) => result.json())
      .then((response) => {
        addUserMenuForDesktop(response);
        removeLogInButtonForDesktop();
        addServersMenuItemForMobile();
        replaceLogInWithLogOutForMobile();
      });
  };
  
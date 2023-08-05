# -*- sh -*-
pkgname=linca
pkgver=0.1.0
pkgrel=1
arch=('any')
depends=('python' 'inotify-tools')
source=('setup.py' 'linca.py')
md5sums=('SKIP'
         'SKIP')

package() {
  cd $srcdir
  python setup.py install --root="$pkgdir" --prefix="/usr"
}

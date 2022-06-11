<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInit61918da48115636221c461d9e2172968
{
    public static $prefixLengthsPsr4 = array (
        'E' => 
        array (
            'EasyPost\\' => 9,
        ),
    );

    public static $prefixDirsPsr4 = array (
        'EasyPost\\' => 
        array (
            0 => __DIR__ . '/..' . '/easypost/easypost-php/lib/EasyPost',
        ),
    );

    public static $classMap = array (
        'Composer\\InstalledVersions' => __DIR__ . '/..' . '/composer/InstalledVersions.php',
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixLengthsPsr4 = ComposerStaticInit61918da48115636221c461d9e2172968::$prefixLengthsPsr4;
            $loader->prefixDirsPsr4 = ComposerStaticInit61918da48115636221c461d9e2172968::$prefixDirsPsr4;
            $loader->classMap = ComposerStaticInit61918da48115636221c461d9e2172968::$classMap;

        }, null, ClassLoader::class);
    }
}

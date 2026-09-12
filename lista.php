<?php
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate');
header('Pragma: no-cache');

$dir      = __DIR__ . '/canzoni';
$extAudio = ['mp3','m4a','wav','ogg','flac','aac','opus'];
$extImg   = ['jpg','jpeg','png','webp','gif'];
$songs    = [];

if (is_dir($dir)) {
    foreach (scandir($dir) as $f) {
        if ($f === '.' || $f === '..') continue;

        $path = $dir . '/' . $f;
        if (!is_file($path)) continue;

        $ext = strtolower(pathinfo($f, PATHINFO_EXTENSION));
        if (!in_array($ext, $extAudio)) continue;

        // Nome file senza estensione
        $base = pathinfo($f, PATHINFO_FILENAME);

        // Prova a leggere "Artista - Titolo"
        $artist = 'Artista sconosciuto';
        $title  = $base;
        if (strpos($base, ' - ') !== false) {
            list($artist, $title) = explode(' - ', $base, 2);
        }

        // Cerca una copertina con lo stesso nome (in /cover o in /canzoni)
        $cover = '';
        foreach ($extImg as $ce) {
            if (file_exists(__DIR__ . '/cover/' . $base . '.' . $ce)) {
                $cover = 'cover/' . rawurlencode($base) . '.' . $ce;
                break;
            }
            if (file_exists($dir . '/' . $base . '.' . $ce)) {
                $cover = 'canzoni/' . rawurlencode($base) . '.' . $ce;
                break;
            }
        }

        $songs[] = [
            'title'  => trim($title),
            'artist' => trim($artist),
            'src'    => 'canzoni/' . rawurlencode($f),
            'cover'  => $cover
        ];
    }

    // Ordine alfabetico per titolo
    usort($songs, fn($a, $b) => strcasecmp($a['title'], $b['title']));
}

echo json_encode($songs, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);